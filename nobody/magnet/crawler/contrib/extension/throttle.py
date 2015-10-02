# -*- coding: utf-8 -*-

from scrapy.contrib.throttle import AutoThrottle
from scrapy.exceptions import NotConfigured
from scrapy import signals


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
        self.mindelay = self._min_delay(spider)
        self.maxdelay = self._max_delay(spider)
        spider.download_delay = self._start_delay(spider)

    def _start_delay(self, spider):
        return max(self.mindelay, self.crawler.settings.getfloat('AUTOTHROTTLE_START_DELAY', 0.5))

    def _adjust_delay(self, slot, latency, response):
        super(CustomThrottle, self)._adjust_delay(slot, latency, response)

        # if response.status == 500:
        #     new_delay = min(slot.delay*2, self.maxdelay)
        #     slot.delay = new_delay
