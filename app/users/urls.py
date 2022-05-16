from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserCreateViewSet, UserTokensList

router = DefaultRouter()
router.register(r'', UserViewSet)
router.register(r'', UserCreateViewSet)

tokens_router = DefaultRouter()
tokens_router.register('tokens', UserTokensList, 'tokens')

urlpatterns = [
    *tokens_router.urls,
    *router.urls
]
