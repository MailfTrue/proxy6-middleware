from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Payment(models.Model):
    notification_type = models.CharField(max_length=32)
    operation_id = models.CharField(max_length=32, primary_key=True)
    amount = models.FloatField(null=True)
    withdraw_amount = models.FloatField(null=True)
    currency = models.CharField(max_length=8)
    datetime = models.DateTimeField()
    sender = models.CharField(max_length=32, null=True, blank=True)
    label = models.CharField(max_length=64, null=True, blank=True)
    sha1_hash = models.CharField(max_length=128)
    test_notification = models.BooleanField(default=False)
    codepro = models.BooleanField(default=False)
    unaccepted = models.BooleanField(default=False)
    raw_data = models.JSONField(null=True)
    counted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.operation_id} {self.amount}"
