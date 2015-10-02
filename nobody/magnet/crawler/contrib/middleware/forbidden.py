# -*- coding: utf-8 -*-

import urlparse

from scrapy import log
from scrapy.exceptions import NotConfigured
from scrapy.utils.response import response_status_message

from magnet.crawler.contrib.store import r


FORBIDDEN_KEY = 'spider:forbidden:link'


class ForbiddenMiddleware(object):

    def __init__(self, settings, server, key):
        if not settings.getbool('FORBIDDEN_ENABLED'):
            raise NotConfigured
        self.server = server
        self.key = key
        self.forbidden_http_codes = set(int(x) for x in settings.getlist('FORBIDDEN_HTTP_CODES'))
        self.redis_key = settings.get('REDIS_KEY')

    @classmethod
    def from_settings(cls, settings):
        server = r
        key = settings.get('FORBIDDEN_KEY', FORBIDDEN_KEY)
        return cls(settings, server, key)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def process_response(self, request, response, spider):
        if response.status in self.forbidden_http_codes:
            reason = response_status_message(response.status)
            self._forbidden(request, reason, spider)

        return response

    def _forbidden(self, request, reason, spider):
        """
        http://www.douban.com/misc/sorry?
            original-url=http%3A%2F%2Fwww.douban.com%2Fgroup%2Fasshole%2Fmembers%3Fstart%3D9590
        """
        try:
            params = urlparse.parse_qs(urlparse.urlparse(request.url).query)
            url = params['original-url'][0]
        except (KeyError, IndexError):
            url = request.url

        _ = self.server.sadd(self.key, url)

        # 等现有队列中request抓取后, 再重新抓一次forbidden的.
        # if self.redis_key:
        #     self.server.lpush(self.redis_key, url)

        log.msg(message='(spider:forbidden:link) - %s' % url,
                level=log.DEBUG)
