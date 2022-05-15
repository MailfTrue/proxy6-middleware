from django.urls import path
from .views import CountriesAPIView, GetPriceAPIView, GetCountAPIView, ListProxyAPIView


urlpatterns = [
    path("countries", CountriesAPIView.as_view()),
    path("price", GetPriceAPIView.as_view()),
    path("count", GetCountAPIView.as_view()),
    path("list", ListProxyAPIView.as_view()),
]