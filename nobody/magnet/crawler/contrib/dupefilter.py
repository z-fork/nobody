# -*- coding: utf-8 -*-

from scrapy import log
from scrapy.dupefilter import BaseDupeFilter
from scrapy.utils.request import request_fingerprint

from magnet.crawler.contrib.store import r
from magnet.crawler import settings


DUPEFILTER_KEY = 'spider:dupefilter:request'


class RFPDupeFilter(BaseDupeFilter):

    def __init__(self, server, key, forbidden_key=None):
        self.server = server
        self.key = key
        self.forbidden_key = forbidden_key or getattr(settings, 'FORBIDDEN_KEY')

    @classmethod
    def from_settings(cls, settings):
        server = r
        key = settings.get('DUPEFILTER_KEY', DUPEFILTER_KEY)
        forbidden_key = settings.get('FORBIDDEN_KEY')
        return cls(server, key, forbidden_key)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):
        fp = request_fingerprint(request)
        added = self.server.sadd(self.key, fp)

        # if not added:
        #     if self.forbidden_key and request.url in self.server.smembers(self.forbidden_key):
        #         self.server.srem(self.forbidden_key, request.url)
        #         log.msg(message='(spider:dupefilter:request) - (forbidden) - %s' % request.url,
        #                 level=log.DEBUG)
        #         return added
        #
        #     log.msg(message='(spider:dupefilter:request) - %s' % request.url,
        #             level=log.DEBUG)

        return not added

    def close(self, reason):
        self.clear()

    def clear(self):
        self.server.delete(self.key)
