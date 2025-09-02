from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import UserViewSet, UserTokensList

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

tokens_router = SimpleRouter()
tokens_router.register('tokens', UserTokensList, 'tokens')

urlpatterns = [
    *tokens_router.urls,
    *router.urls
]
