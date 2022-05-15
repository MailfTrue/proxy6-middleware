from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserCreateViewSet

router = DefaultRouter()
router.register(r'', UserViewSet)
router.register(r'', UserCreateViewSet)

urlpatterns = router.urls
