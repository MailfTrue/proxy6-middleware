from rest_framework import serializers
from .models import Payment
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
