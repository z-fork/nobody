# -*- coding: utf-8 -*-


from base import BaseCrawler
from magnet.crawler.contrib.store import r
from magnet.crawler import settings


class ProxyCrawler(BaseCrawler):
    name = 'proxy'

    redis_key = getattr(settings, 'REDIS_KEY', 'spider:start_urls')

    start_urls = [
        'http://free-proxy-list.net/',
    ]

    _PROXY_PATTERN = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\<\/td\><td\>(\d{2,5})\<\/td\>'

