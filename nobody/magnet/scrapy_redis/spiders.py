# -*- coding: utf-8 -*-

from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from scrapy.utils.misc import load_object

from magnet.crawler import settings
from magnet.crawler.contrib.store import r


class RedisMixin(object):

    redis_key = None  # use default '<spider>:start_urls'

    def setup_redis(self):
        if not self.redis_key:
            self.redis_key = '%s:start_urls' % self.name
        self.server = r
        # idle signal is called when the spider has no requests left,
        # that's when we will schedule new requests from redis queue
        self.crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
        self.log("Reading URLs from redis list '%s'" % self.redis_key)

    def next_request(self):
        try:
            queue_cls = load_object(getattr(settings, 'SCHEDULER_QUEUE_CLASS'))
        except ValueError:
            queue_cls = None
        queue_key = getattr(settings, 'SCHEDULER_QUEUE_KEY')

        if queue_key and queue_cls:
            queue = queue_cls(self.server, self, queue_key)
            i = 0
            while True:
                url = self.server.lpop(self.redis_key)
                i += 1
                if not url or i > 500:
                    break
                request = self.make_requests_from_url(url)
                queue.push(request)
        else:
            url = self.server.lpop(self.redis_key)
            if url:
                return self.make_requests_from_url(url)

    def schedule_next_request(self):
        req = self.next_request()
        if req:
            self.crawler.engine.crawl(req, spider=self)

    def spider_idle(self):
        self.schedule_next_request()
        raise DontCloseSpider
