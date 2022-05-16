from rest_framework import status


def make_user_proxy_descr(user):
    return None
    return f"user#{user.id}"


def get_proxy6_http_status(resp):
    return status.HTTP_200_OK if resp.get("status", "") == "yes" else status.HTTP_400_BAD_REQUEST
