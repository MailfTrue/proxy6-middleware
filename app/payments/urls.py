from django.urls import path
from .views import YoomoneyHook


urlpatterns = [
    path('yoomoney/hook/', YoomoneyHook.as_view()),
]