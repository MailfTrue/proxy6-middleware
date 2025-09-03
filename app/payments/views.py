import hashlib
import re
import hmac
import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import F
from django.db import transaction
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from app.payments.helpers import confirm_cryptobot_payment

from .models import Payment, CryptoBotPayment
from .serializers import CryptoBotPaymentCreatedSerializer, PaymentSerializer, CryptoBotPaymentSerializer, CryptoBotPaymentCreateSerializer

import logging

logger = logging.getLogger(__name__)

User = get_user_model()
USER_ID_REGEX = re.compile(
    r'^user_(?P<user_id>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})$'
)


class PaymentsList(ListAPIView):
    serializer_class = PaymentSerializer
    pagination_class = None

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


class CryptoBotPaymentsList(ListAPIView):
    serializer_class = CryptoBotPaymentSerializer
    pagination_class = None

    def get_queryset(self):
        return CryptoBotPayment.objects.filter(user=self.request.user)


class CryptoBotPaymentCreate(APIView):

    def _create_invoice(self, data):
        import httpx
        client = httpx.Client(
            base_url=settings.CRYPTOBOT_URL,
            headers={
                "Crypto-Pay-API-Token": settings.CRYPTOBOT_TOKEN
            }
        )
        response = client.post(
            "/api/createInvoice", 
            json={
                "currency_type": data["currency_type"],
                "amount": str(data["amount"]),
                "asset": data["crypto_asset"] if data["currency_type"] == "crypto" else None,
                "fiat": data["fiat_asset"] if data["currency_type"] == "fiat" else None,
            }
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to create invoice: {e.response.text}")
            raise serializers.ValidationError("Failed to create invoice")
        response_data = response.json()
        response_result = response_data["result"]
        payment = CryptoBotPayment.objects.create(
            user=self.request.user,
            invoice_id=response_result["invoice_id"],
            hash=response_result["hash"],
            currency_type=response_result["currency_type"],
            amount=response_result["amount"],
            crypto_asset=response_result.get("asset"),
            fiat_asset=response_result.get("fiat"),
            invoice_raw_data=response_result,
        )
        return payment, response_result["bot_invoice_url"]

    def post(self, request):
        serializer = CryptoBotPaymentCreateSerializer(data=request.data)
        if serializer.is_valid():
            payment, url = self._create_invoice(serializer.validated_data)
            response_serializer = CryptoBotPaymentCreatedSerializer(data={
                "url": url, 
                "payment": CryptoBotPaymentSerializer(payment).data,
            })
            response_serializer.is_valid()
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CryptoBotPaymentWebhook(APIView):
    authentication_classes = []
    permission_classes = []

    def _verify_signature(self, request):
        """Проверяет подпись вебхука от CryptoBot"""
        try:
            # Получаем подпись из заголовков
            signature = request.headers.get('crypto-pay-api-signature')
            if not signature:
                logger.warning("No crypto-pay-api-signature header found")
                return False
            
            # Получаем токен из настроек (должен быть добавлен в settings)
            token = getattr(settings, 'CRYPTOBOT_TOKEN', '45246:AA5GI4yj6cFK4beikmRcyyKMzrSIpiEMSHy')
            
            # Создаем секретный ключ как SHA256 хеш токена
            secret = hashlib.sha256(token.encode()).digest()
            
            # Получаем тело запроса как JSON строку
            body_string = json.dumps(request.data, separators=(',', ':'))
            
            # Создаем HMAC-SHA256 подпись
            expected_signature = hmac.new(
                secret, 
                body_string.encode(), 
                hashlib.sha256
            ).hexdigest()
            
            # Сравниваем подписи
            is_valid = hmac.compare_digest(expected_signature, signature)
            
            if not is_valid:
                logger.warning(f"Invalid signature. Expected: {expected_signature}, Got: {signature}")
            
            return is_valid
            
        except Exception as e:
            logger.error(f"Error verifying signature: {e}")
            return False

    def post(self, request):
        from pprint import pprint
        pprint(request.data)
        
        # Всегда отвечаем 200 OK, даже при ошибках
        try:
            # Проверяем подпись вебхука
            if not self._verify_signature(request):
                logger.warning("Webhook signature verification failed")
                return Response(status=status.HTTP_200_OK)
            
            # Проверяем тип обновления
            update_type = request.data.get('update_type')
            if update_type != 'invoice_paid':
                logger.info(f"Received webhook with update_type: {update_type}, ignoring")
                return Response(status=status.HTTP_200_OK)
            
            payload = request.data.get('payload', {})
            
            # Проверяем статус платежа
            payment_status = payload.get('status')
            if payment_status != 'paid':
                logger.info(f"Payment status is not 'paid': {payment_status}")
                return Response(status=status.HTTP_200_OK)
            
            # Проверяем валюту - должна быть RUB
            fiat = payload.get('fiat')
            if fiat != 'RUB':
                logger.warning(f"Payment currency is not RUB: {fiat}")
                return Response(status=status.HTTP_200_OK)
            
            # Получаем invoice_id для поиска платежа
            invoice_id = payload.get('invoice_id')
            if not invoice_id:
                logger.error("No invoice_id in webhook payload")
                return Response(status=status.HTTP_200_OK)
            
            # Находим платеж в базе данных
            try:
                payment = CryptoBotPayment.objects.get(invoice_id=invoice_id)
            except CryptoBotPayment.DoesNotExist:
                logger.error(f"Payment with invoice_id {invoice_id} not found")
                return Response(status=status.HTTP_200_OK)
            
            # Проверяем, что платеж еще не обработан
            if payment.status == CryptoBotPayment.Status.PAID:
                logger.info(f"Payment {invoice_id} already processed")
                return Response(status=status.HTTP_200_OK)
            
            # Получаем сумму для зачисления (в рублях)
            amount_to_credit = float(payload.get('amount', 0))
            
            if amount_to_credit <= 0:
                logger.error(f"Invalid amount to credit: {amount_to_credit}")
                return Response(status=status.HTTP_200_OK)
            
            # Обновляем статус платежа и зачисляем средства пользователю
            confirm_cryptobot_payment(payment.invoice_id)
            return Response(status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return Response(status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_200_OK)
