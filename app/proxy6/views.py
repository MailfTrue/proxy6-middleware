from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from rest_framework.views import APIView
from rest_framework.response import Response
from .integrations import proxy6_client
from . import utils

class CountriesAPIView(APIView):

    @method_decorator(cache_page(60*60))
    def get(self, request, format=None):
        resp = proxy6_client.getcountry(
            request.user,
            **request.query_params.dict(),
        )
        return Response(resp, status=utils.get_proxy6_http_status(resp))


class GetPriceAPIView(APIView):

    @method_decorator(cache_page(60*10))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, format=None):
        resp = proxy6_client.getprice(
            request.user,
            version=4, 
            **request.query_params.dict(),
        )
        return Response(resp, status=utils.get_proxy6_http_status(resp))


class GetCountAPIView(APIView):

    @method_decorator(cache_page(60*5))
    def get(self, request, format=None):
        resp = proxy6_client.getcount(
            request.user,
            **request.query_params.dict(),
        )
        return Response(resp, status=utils.get_proxy6_http_status(resp))


class ListProxyAPIView(APIView):
    def get(self, request, format=None):
        resp = proxy6_client.getproxy(
            request.user, 
            nokey=True, 
            descr=utils.make_user_proxy_descr(request.user),
            **request.query_params.dict(),
        )
        return Response(resp, status=utils.get_proxy6_http_status(resp))


class BuyProxyAPIView(APIView):
    def get(self, request, format=None):
        resp = proxy6_client.buy(
            request.user,
            **request.query_params.dict(),
        )
        return Response(resp, status=utils.get_proxy6_http_status(resp))


class DeleteProxyAPIView(APIView):
    def get(self, request, format=None):
        resp = proxy6_client.delete(
            request.user, 
            descr=utils.make_user_proxy_descr(request.user), 
            **request.query_params.dict(),
        )
        return Response(resp, status=utils.get_proxy6_http_status(resp))


class ProlongProxyAPIView(APIView):
    def get(self, request, format=None):
        resp = proxy6_client.prolong(
            request.user, 
            nokey=True, 
            **request.query_params.dict(),
        )
        return Response(resp, status=utils.get_proxy6_http_status(resp))
