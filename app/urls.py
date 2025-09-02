from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path("users/", include("app.users.urls")),
        path("proxy/", include("app.proxy6.urls")),
        path("payments/", include("app.payments.urls")),
    ])),
    path('api/jwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + (
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + 
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

