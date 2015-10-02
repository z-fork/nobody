# -*- coding: utf-8 -*-

from scrapy import log
from scrapy.contrib.spiders import CrawlSpider

from magnet.scrapy_redis.spiders import RedisMixin
from magnet.crawler.contrib.store import r
from magnet.crawler import settings


class BaseCrawler(RedisMixin, CrawlSpider):
    name = 'base_crawler'
    redis_key = 'base_crawler:start_urls'

    DUPEFILTER_LINK_KEY = 'spider:dupefilter:link'

    def __init__(self, *args, **kwargs):
        super(BaseCrawler, self).__init__(*args, **kwargs)

    def process_links(self, links):
        def filter_link(link):
            key = getattr(settings, 'DUPEFILTER_LINK_KEY') or self.DUPEFILTER_LINK_KEY
            added = r.sadd(key, link.url)

            if not added:
                forbidden_key = getattr(settings, 'FORBIDDEN_KEY')
                if forbidden_key and link.url in self.server.smembers(forbidden_key):
                    return not added

                log.msg(message='(spider:dupefilter:link) - %s' % link.url,
                        level=log.DEBUG)

            return added

        return filter(filter_link, links)

    def set_crawler(self, crawler):
        super(BaseCrawler, self).set_crawler(crawler)
        self.setup_redis()
