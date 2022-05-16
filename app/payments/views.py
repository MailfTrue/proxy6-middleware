import hashlib
import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import F
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer
from .integrations import Yoomoney

from collections import defaultdict

User = get_user_model()
USER_ID_REGEX = re.compile(
    r'^user_(?P<user_id>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})$'
)
yoomoney = Yoomoney(settings.YOOMONEY_ACCESS_TOKEN)


class YoomoneyHook(CreateAPIView):
    permission_classes = []
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        try:
            hash_string_parts = [
                request.data['notification_type'],
                request.data['operation_id'],
                request.data['amount'],
                request.data['currency'],
                request.data['datetime'],
                request.data['sender'],
                request.data['codepro'],
                settings.YOOMONEY_WEBHOOK_SECRET,
                request.data['label']
            ]
            hash_string = '&'.join(k or '' for k in hash_string_parts)
            hashed_string = hashlib.sha1(hash_string.encode()).hexdigest()
            if hashed_string != request.data['sha1_hash']:
                return Response('Hash error', status=status.HTTP_401_UNAUTHORIZED)

            instance = Payment.objects.filter(operation_id=request.data['operation_id']).first()
            serializer = self.get_serializer(data=request.data, instance=instance)
            serializer.is_valid(raise_exception=True)
            payment = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            response = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

            user_id_match = USER_ID_REGEX.match(request.data['label'])
            if user_id_match and request.data['unaccepted'] != 'true' and not payment.counted:
                user_id = user_id_match['user_id']
                if User.objects.filter(id=user_id).exists():
                    User.objects.filter(id=user_id).update(balance=F('balance') + float(request.data['amount']))
                    payment.user_id = user_id
                    payment.counted = True
                    payment.save()
            return response
        except Exception as e:
            raise e


class PaymentsList(ListAPIView):
    serializer_class = PaymentSerializer
    pagination_class = None

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

