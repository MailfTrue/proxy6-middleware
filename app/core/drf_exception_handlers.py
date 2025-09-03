from rest_framework.response import Response
from rest_framework.views import exception_handler

from app.proxy6.integrations.proxy6 import Proxy6ClientError

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is None:
        if isinstance(exc, Proxy6ClientError):
            response = Response(
                exc.detail,
                status=500,
            )

    return response
