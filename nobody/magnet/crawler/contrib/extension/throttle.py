# -*- coding: utf-8 -*-

import logging

from scrapy.contrib.throttle import AutoThrottle
from scrapy.exceptions import NotConfigured
from scrapy import signals

from proxies.utils import add_or_update


class CustomThrottle(AutoThrottle):
    def __init__(self, crawler):
        try:
            super(CustomThrottle, self).__init__(crawler)
        except NotConfigured:
            if not crawler.settings.getbool('CUSTOM_AUTOTHROTTLE_ENABLED'):
                raise NotConfigured

            self.debug = crawler.settings.getbool("CUSTOM_AUTOTHROTTLE_DEBUG")

            crawler.signals.connect(self._spider_opened, signal=signals.spider_opened)
            crawler.signals.connect(self._response_downloaded, signal=signals.response_downloaded)

    def _spider_opened(self, spider):
        spider.download_delay = 0

    def _response_downloaded(self, response, request, spider):
        key, slot = self._get_slot(request, spider)
        latency = request.meta.get('download_latency') * 1000
        proxy = request.meta.get('proxy')

        if latency is None or slot is None or proxy is None:
            return

        if self.debug:
            size = len(response.body)
            conc = len(slot.transferring)
            msg = "slot: %s | conc: %2d | latency:%5d ms | size: %6d bytes | proxy:%s" \
                  % (key, conc, latency, size, proxy)
            spider.log(msg, level=logging.DEBUG)

        add_or_update(proxy, latency)
