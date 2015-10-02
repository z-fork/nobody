# -*- coding: utf-8 -*-

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from proxy.controls import rq_get_proxy


@api_view(['GET'])
def get_proxy(request):
    proxy = rq_get_proxy()

    if not proxy:
        return Response(
            {
                "error_code": 10086,
                "detail": "proxy is not available"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response({
        'proxy': proxy,
    })
