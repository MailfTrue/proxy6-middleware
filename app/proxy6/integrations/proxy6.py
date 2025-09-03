from django.db import transaction
from django.db.models.functions import Now
import httpx
from django.conf import settings

from app.proxy6.models import PurchasedProxy
from app.proxy6.utils import make_user_proxy_descr
from app.payments.helpers import write_off_user_balance
from app.utils import send_tg_notify


PROXY6_VERSION = 4


class Proxy6ClientError(Exception):
    default_detail = "Proxy error"
    default_code = 'invalid'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        self.detail = detail
        self.code = code


class Proxy6Client:
    API_METHODS = (
        'getprice',
        'getcount',
        'getcountry',
        'getproxy',
        'settype',
        'setdescr',
        'buy',
        'prolong',
        'delete',
        'check'
    )

    def __init__(self, api_key):
        self.__api_key = api_key
        self.client = httpx.Client(base_url=f"https://px6.me/api/{api_key}", timeout=30)

    def __getattr__(self, item):
        if item in self.API_METHODS:
            def __method(user, **params):
                return self.api_call(user, item, params)
            return __method
        raise AttributeError(f"Proxy6Client has no attribute {item}")

    def getproxy(self, user, **params):
        return self.api_call(user, "getproxy", params)

    def getprice(self, user, **params):
        resp = self.api_call(user, "getprice", params)
        resp['price'] = float(resp['price']) * settings.PRICE_MARKUP_FACTOR
        resp['price_single'] = float(resp['price_single']) * settings.PRICE_MARKUP_FACTOR
        return resp

    def buy(self, user, **params):
        params['version'] = PROXY6_VERSION
        params['nokey'] = True
        params['descr'] = make_user_proxy_descr(user)
        price = self.getprice(user, **params)['price']
        if price > user.balance:
            raise Proxy6ClientError({'detail': "Not enough money"}, code='not_enough_money')
        resp = self.api_call(user, "buy", params)
        resp['price'] = float(resp['price']) * settings.PRICE_MARKUP_FACTOR
        with transaction.atomic():
            PurchasedProxy.objects.bulk_create([
                PurchasedProxy(
                    user=user, 
                    proxy_id=proxy['id'], 
                    period=params['period'],
                ) for proxy in resp['list']
            ])

            proxy_ids = ','.join([proxy['id'] for proxy in resp['list']])
            description = (
                f"Purchase {params['count']} proxies "
                f"for {params['period']} days: "
                f"{proxy_ids}"
            )
            write_off_user_balance(
                user, 
                resp['price'], 
                description=description,
            )
        return resp

    def prolong(self, user, **params):
        proxy_ids = params['ids'].split(',')
        price = self.getprice(
            user,
            count=len(proxy_ids),
            period=params['period'],
            version=PROXY6_VERSION,
        )['price']
        if price > user.balance:
            raise Proxy6ClientError({'detail': "Not enough money"}, code='not_enough_money')
        resp = self.api_call(user, "prolong", params)
        resp['price'] = float(resp['price']) * settings.PRICE_MARKUP_FACTOR

        description = (
            f"Prolongation {len(proxy_ids)} proxies "
            f"for {params['period']} days: "
            f"{', '.join(proxy_ids)}"
        )
        write_off_user_balance(user, resp['price'], description=description)
        return resp

    def delete(self, user, **params):
        resp = self.api_call(user, "delete", params)
        (
            PurchasedProxy.objects
            .filter(
                deleted_at__isnull=True,
                proxy_id__in=params['ids'].split(','), 
                user=user,
            )
            .update(deleted_at=Now())
        )
        return resp

    def api_call(self, user, method, params=None, hide_user_data=True):
        data = self.client.get(method, params=params).json()
        if hide_user_data:
            for key in ["user_id", "balance", "currency"]:
                if key in data:
                    del data[key]
        
        if 'error_id' in data:
            error_descriptions = {
                30: 'Error unknown - Unknown error',
                100: 'Error key - Authorization error, invalid key',
                105: 'Error ip - API access from incorrect IP (if restriction enabled) or invalid IP address format',
                110: 'Error method - Invalid method',
                200: 'Error count - Proxy count error, invalid count specified or missing',
                210: 'Error period - Period error, invalid number of days specified or missing',
                220: 'Error country - Country error, invalid country specified (countries should be in iso2 format) or missing',
                230: 'Error ids - Proxy ID list error. Proxy IDs must be comma-separated',
                240: 'Error version - Invalid proxy version specified',
                250: 'Error descr - Technical comment error, invalid or missing',
                260: 'Error type - Proxy type (protocol) error, invalid or missing',
                270: 'Error port - Proxy port error, invalid or missing',
                280: 'Error proxy str - Proxy string error for check method, invalid format',
                300: 'Error active proxy allow - Proxy count error. Occurs when trying to buy more proxies than available on the service',
                400: 'Error no money - Balance error. Insufficient funds on your balance for requested number of proxies',
                404: 'Error not found - Search error. Requested item not found',
                410: 'Error price - Price calculation error. Final price is less than or equal to zero'
            }
            data['error_descr'] = error_descriptions.get(data['error_id'], error_descriptions[30])
            send_tg_notify(
                f"Proxy6 error: {data['error_descr']}\n"
                f"User: {user.username}\n"
                f"Method: {method}\n"
                f"Params: {params}"
            )
            raise Proxy6ClientError({'detail': data['error_descr']}, code=data['error_id'])

        return data


proxy6_client = Proxy6Client(settings.PROXY6_API_KEY)
