from django.db import models
from django.conf import settings


class PurchasedProxy(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    proxy_id = models.CharField(max_length=16)
    period = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.proxy_id}"
