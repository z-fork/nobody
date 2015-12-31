# -*- coding: utf-8 -*-

import re

from scrapy.contrib.spiders import CrawlSpider
from scrapy import Request

from proxies.crawler.items import RedisItem


class ProxySpider(CrawlSpider):
    name = 'proxy'

    _TEST_URL = 'http://www.douban.com/'

    _FREE_PROXY_PATTERN = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\<\/td\><td\>(\d{2,5})\<\/td\>'
    _HOST_PORT_PATTERN = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{2,5})'

    _URLS = {
        _FREE_PROXY_PATTERN: ['http://free-proxy-list.net/', ],
        _HOST_PORT_PATTERN: ['http://proxy-list.org/english/index.php?p=%s' % i for i in range(1, 11)],
    }

    def start_requests(self):
        for pattern, urls in self._URLS.iteritems():
            meta = {'pattern': pattern}
            for url in urls:
                yield Request(url, meta=meta, dont_filter=True)

    def parse(self, response):
        meta = response.meta
        htm = response.body

        proxies = re.findall(meta['pattern'], htm, re.I)

        for p in proxies:
            proxy = 'http://%s:%s' % p if isinstance(p, tuple) else 'http://%s' % p
            meta = {
                'proxy': proxy
            }
            yield Request(self._TEST_URL, meta=meta, callback=self.parse_detail, dont_filter=True)

    def parse_detail(self, response):
        meta = response.meta

        yield RedisItem({
            'proxy': meta['proxy'],
            'priority': int(meta['download_latency'] * 1000)
        })
