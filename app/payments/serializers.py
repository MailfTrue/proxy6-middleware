from rest_framework import serializers
from .models import Payment, CryptoBotPayment
import json


class PaymentSerializer(serializers.ModelSerializer):

    def __init__(self, *args, data=None, **kwargs):
        if data:
            data = data.dict()
            data['raw_data'] = json.dumps(data)
        super().__init__(*args, data=data, **kwargs)

    class Meta:
        model = Payment
        fields = (
            'notification_type',
            'operation_id',
            'amount',
            'withdraw_amount',
            'currency',
            'datetime',
            'sender',
            'label',
            'sha1_hash',
            'test_notification',
            'codepro',
            'unaccepted',
            'raw_data'
        )


class CryptoBotPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoBotPayment
        fields = (
            "invoice_id",
            "hash",
            "currency_type",
            "crypto_asset",
            "fiat_asset",
            "amount",
            "status",
            "created_at",
            "updated_at",
        )



class CryptoBotPaymentCreatedSerializer(serializers.Serializer):
    url = serializers.URLField()
    payment = CryptoBotPaymentSerializer()



class CryptoBotPaymentCreateSerializer(serializers.Serializer):
    currency_type = serializers.ChoiceField(choices=CryptoBotPayment.CurrencyType.choices)
    crypto_asset = serializers.ChoiceField(choices=CryptoBotPayment.CryptoAsset.choices, required=False)
    fiat_asset = serializers.ChoiceField(choices=CryptoBotPayment.FiatAsset.choices, required=False)
    amount = serializers.DecimalField(max_digits=16, decimal_places=2)

    def validate(self, attrs):
        if attrs["currency_type"] == CryptoBotPayment.CurrencyType.CRYPTO:
            if not attrs.get("crypto_asset"):
                raise serializers.ValidationError("Crypto asset is required")
        elif attrs["currency_type"] == CryptoBotPayment.CurrencyType.FIAT:
            if not attrs.get("fiat_asset"):
                raise serializers.ValidationError("Fiat asset is required")
        return attrs
