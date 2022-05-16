from django.urls import path
from .views import YoomoneyHook, PaymentsList


urlpatterns = [
    path('yoomoney/hook/', YoomoneyHook.as_view()),
    path('', PaymentsList.as_view()),
]
