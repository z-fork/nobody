# -*- coding: utf-8 -*-

import re
import time
import urllib

import requests

from nobody.libs.store import r as r_store
from nobody.libs.queue import RedisQueue
from proxy.models import NobodyProxy


rq = RedisQueue(r_store, 'proxy')


class FetchProxy(object):
    PROXY_SITE = [
        ('http://free-proxy-list.net/', '(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\<\/td\><td\>(\d{2,5})\<\/td\>', '', ''),
    ] + [
        ('http://proxy-list.org/english/index.php?p=%s' % i, '', '', '') for i in range(1, 11)
    ]

    HOST_PORT_PATTERN = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{2,5})'

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0',
        'Referer': 'https://www.google.com.hk/',
    }

    TEST_URL = 'http://www.douban.com'
    TIME_OUT = 1

    def __init__(self, url, host_reg='', mode='', rgx=''):
        self.url = url
        self.proxy_reg = host_reg or self.HOST_PORT_PATTERN
        self.fetch_mode = mode
        self.content_reg = rgx

    def _fetch_site_by_requests(self, url):
        try:
            r = requests.get(url, headers=self.HEADERS)

            if r.status_code != 200:
                return

            return r.content
        except Exception as e:
            _ = e.message

    def _fetch_url(self, url):
        try:
            content = self._fetch_site_by_requests(url)

            scheme, url = urllib.splittype(self.url)
            host, _ = urllib.splithost(url)

            url = re.findall(self.content_reg, content, re.I)[0]

            return url if 'http://' in url else 'http://%s:%s' % (host, url)
        except Exception as e:
            _ = e.message
            return

    def fetch_proxy(self):
        if self.content_reg:
            url = self._fetch_url(self.url)
        else:
            url = self.url

        content = self._fetch_site_by_requests(url)

        proxies = re.findall(self.proxy_reg, content, re.I)

        proxies_priority = {}

        for p in proxies:
            proxy = 'http://%s:%s' % p if isinstance(p, tuple) else 'http://%s' % p
            priority = self.proxy_test(proxy)

            if priority:
                proxies_priority.update({
                    proxy: priority
                })

        return proxies_priority

    def proxy_test(self, proxy):
        try:
            start = time.time()
            r = requests.get(self.TEST_URL, proxies={'http': proxy}, timeout=self.TIME_OUT)
            return int((time.time() - start) * 100) if r.status_code == 200 else 0
        except Exception as e:
            _ = e.message
            return 0

    def save_proxy(self, proxy, priority):
        NobodyProxy.create(proxy, priority)


def rq_clear_proxy():
    rq.clear()


def rq_get_proxy():
    if rq.empty():
        proxies = NobodyProxy.get_all()

        for proxy in proxies:
            rq.put(proxy)

    return rq.get_nowait()
