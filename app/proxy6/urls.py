from django.urls import path
from . import views


urlpatterns = [
    path("countries", views.CountriesAPIView.as_view()),
    path("price", views.GetPriceAPIView.as_view()),
    path("count", views.GetCountAPIView.as_view()),
    path("list", views.ListProxyAPIView.as_view()),
    path("buy", views.BuyProxyAPIView.as_view()),
    path("delete", views.DeleteProxyAPIView.as_view()),
]
