from collections import defaultdict
from datetime import datetime, timedelta


from app.celery import app
from app.proxy6.models import PurchasedProxy
from app.proxy6.utils import make_user_proxy_descr
from .integrations import proxy6_client
from app.users.models import User


@app.task
def prolong_users_proxies():
    user_ids = User.objects.values_list('id', flat=True)
    for user_id in user_ids:
        prolong_user_proxies.delay(user_id)


@app.task
def prolong_user_proxies(user_id):
    user = User.objects.get(id=user_id)
    proxies = proxy6_client.getproxy(
        user,
        nokey=True,
        descr=make_user_proxy_descr(user),
    )

    need_prolong = []
    now = datetime.now()
    for proxy in proxies['list']:
        date_end = datetime.fromisoformat(proxy['date_end'])
        if date_end - now < timedelta(days=1):
            need_prolong.append(proxy['id'])

    prolong_proxies = (
        PurchasedProxy.objects
        .filter(
            user=user, 
            proxy_id__in=need_prolong,
            deleted_at__isnull=True,
        )
        .values_list('proxy_id', 'period')
    )

    prolong_proxies_by_period = defaultdict(list)
    for proxy_id, period in prolong_proxies:
        prolong_proxies_by_period[period].append(proxy_id)

    for period, proxy_ids in prolong_proxies_by_period.items():
        proxies_ids = ','.join(proxy_ids)
        proxy6_client.prolong(
            user, 
            ids=proxies_ids,
            period=period,
        )

