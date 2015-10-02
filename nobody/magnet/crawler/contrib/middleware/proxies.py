# -*- coding: utf-8 -*-

from proxy.controls import rq_get_proxy


class RotateHttpProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy = rq_get_proxy()
        # proxy = 'http://218.207.212.79:80'
        # proxy = ''
        if proxy:
            request.meta['proxy'] = proxy
