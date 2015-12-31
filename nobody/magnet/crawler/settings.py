# -*- coding: utf-8 -*-

import os
import sys

# 使 Scrapy 与 Django 兼容
_NOBODY_ROOT = os.path.join(os.path.dirname(__file__), '../..')
sys.path.append(_NOBODY_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'nobody.settings'

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

IMAGES_STORE = _NOBODY_ROOT

CONCURRENT_REQUESTS = 16  # 全局并发数, 在外层downloader控制active数
CONCURRENT_REQUESTS_PER_DOMAIN = 8  # 单个domain并发数, 在内层HTTPConnection控制pool大小

SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
SCHEDULER_PERSIST = True
# SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderQueue'
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderStack'

SCHEDULER_QUEUE_KEY = 'spider:requests'
DUPEFILTER_KEY = 'spider:dupefilter:request'
DUPEFILTER_LINK_KEY = 'spider:dupefilter:link'
FORBIDDEN_KEY = 'spider:forbidden:link'
REDIS_KEY = 'spider:start_urls'

DNSCACHE_ENABLED = True  # dns cache in-memory TODO 看下是怎么做的, 能不能分出一个服务?..

DOWNLOADER_DEBUG = True
DOWNLOAD_TIMEOUT = 15
# DOWNLOAD_DELAY = 1

DEPTH_LIMIT = 0  # 无限制深度
# DEPTH_STATS = True
# DEPTH_PRIORITY = 0  # DFS
# DEPTH_PRIORITY = 1  # BFS

DEPTH_STATS_VERBOSE = True  # TODO 确认一下..应该meta中能看到的吧..

# 重定向
REDIRECT_ENABLED = True
REDIRECT_MAX_TIMES = 20

# Forbidden
FORBIDDEN_ENABLED = True
FORBIDDEN_HTTP_CODES = [403, ]

COOKIES_ENABLED = True
COOKIES_DEBUG = False

CUSTOM_AUTOTHROTTLE_ENABLED = True
CUSTOM_AUTOTHROTTLE_DEBUG = True

EXTENSIONS = {
    'crawler.contrib.extension.throttle.CustomThrottle': 10
}

ITEM_PIPELINES = {
    # 'crawler.pipelines.QuestionImagesPipeline': 200,
    'crawler.pipelines.DjangoModelPipeline': 800,
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'crawler.contrib.middleware.useragent.RotateUserAgentMiddleware': 400,
    'crawler.contrib.middleware.redirect.CaptchaRedirectMiddleware': 625,
    'crawler.contrib.middleware.forbidden.ForbiddenMiddleware': 650,
    # 'crawler.contrib.middleware.proxies.RotateHttpProxyMiddleware': 755,
}

DUPEFILTER_CLASS = 'crawler.contrib.dupefilter.RFPDupeFilter'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; rv:32.0) Gecko/20100101 Firefox/32.0'

REDIS_CONF = {
    'host': 'localhost',
    'port': 6379,
    'db': 3
}
