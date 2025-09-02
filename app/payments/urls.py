from django.urls import path, include
from .views import PaymentsList, CryptoBotPaymentsList, CryptoBotPaymentCreate, CryptoBotPaymentWebhook


urlpatterns = [
    path('', PaymentsList.as_view()),
    path('cryptobot/', include([
        path('', CryptoBotPaymentsList.as_view()),
        path('create/', CryptoBotPaymentCreate.as_view()),
        path('webhook/', CryptoBotPaymentWebhook.as_view()),
    ])),
]
