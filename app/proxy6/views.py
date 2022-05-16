from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status
from django.conf import settings
from .integrations import Proxy6Client
from . import utils

proxy6_client = Proxy6Client(settings.PROXY6_API_KEY)


class CountriesAPIView(APIView):

    @method_decorator(cache_page(60*60))
    def get(self, request, format=None):
        return Response(proxy6_client.getcountry(**request.query_params))


class GetPriceAPIView(APIView):

    @method_decorator(cache_page(60*10))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, format=None):
        resp = proxy6_client.getprice(version=4, **request.query_params)
        resp['price'] *= settings.PRICE_MARKUP_FACTOR
        resp['price_single'] *= settings.PRICE_MARKUP_FACTOR
        return Response(resp)


class GetCountAPIView(APIView):

    @method_decorator(cache_page(60*5))
    def get(self, request, format=None):
        return Response(proxy6_client.getcount(**request.query_params))


class ListProxyAPIView(APIView):
    def get(self, request, format=None):
        return Response(proxy6_client.getproxy(nokey=True, descr=utils.make_user_proxy_descr(request.user),
                                               **request.query_params))


class BuyProxyAPIView(APIView):
    def get(self, request, format=None):
        price = proxy6_client.getprice(**request.query_params)['price'] * settings.PRICE_MARKUP_FACTOR
        if price > request.user.balance and False:
            raise APIException("Not enough money")

        resp = proxy6_client.buy(nokey=True, descr=utils.make_user_proxy_descr(request.user),
                                 version=4, **request.query_params)
        return Response(resp, status=utils.get_proxy6_http_status(resp))


class DeleteProxyAPIView(APIView):
    def get(self, request, format=None):
        return Response(proxy6_client.delete(descr=utils.make_user_proxy_descr(request.user), **request.query_params))


class ProlongProxyAPIView(APIView):
    def get(self, request, format=None):
        return Response(proxy6_client.prolong(nokey=True, **request.query_params))
