import logging
from datetime import datetime, timedelta

from app.celery import app
from app.proxy6.helpers import send_prolong_error_notification
from app.proxy6.models import PurchasedProxy
from app.proxy6.utils import make_user_proxy_descr
from .integrations import proxy6_client
from .integrations.proxy6 import Proxy6ClientError
from app.users.models import User

logger = logging.getLogger(__name__)


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

    for proxy_id, period in prolong_proxies:
        try:
            proxy6_client.prolong(
                user, 
                ids=proxy_id,
                period=period,
            )
            logger.info(f"Successfully prolonged proxy {proxy_id} for user {user.username}")
        except Proxy6ClientError as e:
            logger.error(f"Failed to prolong proxy {proxy_id} for user {user.username}: {e}")
            send_prolong_error_notification(user, proxy_id, str(e))

