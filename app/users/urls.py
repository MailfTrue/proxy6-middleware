from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import UserViewSet, UserCreateViewSet, UserTokensList

router = DefaultRouter()
router.register(r'', UserViewSet)
router.register(r'', UserCreateViewSet)

tokens_router = SimpleRouter()
tokens_router.register('tokens', UserTokensList, 'tokens')

urlpatterns = [
    *tokens_router.urls,
    *router.urls
]
