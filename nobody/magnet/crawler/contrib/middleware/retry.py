# -*- coding: utf-8 -*-

import logging

from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware

from proxies.crawler.settings import PRIORITY_RATE
from proxies.utils import get_proxy, get_priority, add_or_update


class ProxyRetryMiddleware(RetryMiddleware):
    def _retry(self, request, reason, spider):
        proxy = request.meta.get('proxy')
        if proxy:
            priority = get_priority(proxy)
            if priority:
                add_or_update(proxy, priority + PRIORITY_RATE)
            proxy = get_proxy()
            if proxy:
                request.meta['proxy'] = proxy
                spider.log('RetryMiddleware used proxy: %s, new proxy: %s' %
                           (request.meta['proxy'], proxy), logging.DEBUG)

        super(ProxyRetryMiddleware, self)._retry(request, reason, spider)
