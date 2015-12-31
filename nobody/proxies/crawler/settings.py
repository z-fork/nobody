# -*- coding: utf-8 -*-

import os
import sys

# 使 Scrapy 与 Django 兼容
_BANKER_ROOT = os.path.join(os.path.dirname(__file__), '../..')
sys.path.append(_BANKER_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'nobody.settings'

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

CONCURRENT_REQUESTS = 50
CONCURRENT_REQUESTS_PER_DOMAIN = 50

DNSCACHE_ENABLED = True

DOWNLOADER_DEBUG = True
DOWNLOAD_TIMEOUT = 10
# DOWNLOAD_DELAY = 1

REDIRECT_ENABLED = False

RETRY_ENABLED = False

COOKIES_ENABLED = False

PROXY_STORE_KEY = 'PROXY:ZSETS'
PROXY_QUEUE_KEY = 'PROXY:QUEUE'

PRIORITY_RATE = 2000
ABANDON_PRIORITY = 30000

ITEM_PIPELINES = {
    'crawler.pipelines.RedisPipeline': 800,
}

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0'
