from django.core.management.base import BaseCommand

from app.proxy6.tasks import prolong_users_proxies


class Command(BaseCommand):
    help = 'Запустить продление всех прокси'

    def handle(self, *args, **options):
        prolong_users_proxies.delay()
        self.stdout.write(self.style.SUCCESS('Задача продления отправлена в Celery'))
