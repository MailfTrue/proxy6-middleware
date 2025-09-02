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


class CryptoBotPayment(models.Model):
    class CurrencyType(models.TextChoices):
        FIAT = "fiat"
        CRYPTO = "crypto"

    class CryptoAsset(models.TextChoices):
        USDT = "USDT"

    class FiatAsset(models.TextChoices):
        RUB = "RUB"

    class Status(models.TextChoices):
        ACTIVE = "active"
        PAID = "paid"
        EXPIRED = "expired"

    invoice_id = models.PositiveIntegerField(primary_key=True)
    hash = models.CharField(max_length=128)
    currency_type = models.CharField(max_length=16, choices=CurrencyType.choices)
    crypto_asset = models.CharField(max_length=16, choices=CryptoAsset.choices, null=True, blank=True)
    fiat_asset = models.CharField(max_length=16, choices=FiatAsset.choices, null=True, blank=True)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)

    invoice_raw_data = models.JSONField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.invoice_id} {self.amount}"
