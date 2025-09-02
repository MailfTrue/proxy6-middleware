from django.contrib import admin
from .models import CryptoBotPayment
from .helpers import confirm_cryptobot_payment


@admin.register(CryptoBotPayment)
class CryptoBotPaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice_id', 'user', 'amount', 'status', 'created_at', 'updated_at')
    list_filter = ('user', 'status', 'created_at', 'updated_at')
    search_fields = ('invoice_id', 'user__username')
    actions = ('confirm_payment',)

    def has_change_permission(self, request, obj=None):
        return False

    @admin.action(description='Confirm payment')
    def confirm_payment(self, request, queryset):
        for payment in queryset:
            confirm_cryptobot_payment(payment.invoice_id)
