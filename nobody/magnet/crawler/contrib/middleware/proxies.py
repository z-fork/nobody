# -*- coding: utf-8 -*-

from proxies.utils import get_proxy


class RotateHttpProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy = get_proxy()
        if proxy:
            request.meta['proxy'] = proxy
