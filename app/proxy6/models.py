from django.db import models
from django.conf import settings


class UserProxy(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    proxy_uid = models.CharField(max_length=16)

