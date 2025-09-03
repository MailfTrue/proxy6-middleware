from decimal import Decimal
from django.db.models import F
from django.db import transaction
import logging

from .models import Payment, CryptoBotPayment
from ..utils import send_tg_notify

logger = logging.getLogger(__name__)

def confirm_cryptobot_payment(payment_id):
    # Обновляем статус платежа и зачисляем средства пользователю
    with transaction.atomic():
        payment = (
            CryptoBotPayment.objects
            .select_for_update()
            .get(invoice_id=payment_id)
        )
        if payment.status == CryptoBotPayment.Status.PAID:
            logger.error(f"Payment {payment_id} already processed")
            raise ValueError(f"Payment {payment_id} already processed")
            return
        payment.status = CryptoBotPayment.Status.PAID
        payment.save()
        
        # Зачисляем средства пользователю
        user = payment.user
        if user:
            user.balance = F('balance') + payment.amount
            user.save()
            
            logger.info(f"Successfully credited {payment.amount} RUB to user {user.id}")
            
            # Отправляем уведомление в Telegram
            try:
                send_tg_notify(
                    f"💰 Пополнение баланса\n"
                    f"Пользователь: {user.username}\n"
                    f"Сумма: {payment.amount} RUB\n"
                    f"Новый баланс: {user.balance} RUB"
                )
            except Exception as e:
                logger.error(f"Failed to send Telegram notification: {e}")
        else:
            logger.error(f"No user associated with payment {payment_id}")


def write_off_user_balance(user, amount):
    amount = Decimal(amount)
    with transaction.atomic():
        user.balance -= amount
        user.save()
        user.refresh_from_db()

        logger.info(f"Successfully wrote off {amount} RUB from user {user.id}")

        try:
            send_tg_notify(
                f"💰 Списание средств\n"
                f"Пользователь: {user.username}\n"
                f"Сумма: {amount} RUB\n"
                f"Новый баланс: {user.balance} RUB"
            )
        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {e}")
