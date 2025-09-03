import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

from django import setup
setup()

from app.proxy6.tasks import prolong_user_proxies

prolong_user_proxies("d353fa6f-670e-43a6-a844-12426af2df00")
