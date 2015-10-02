# -*- coding: utf-8 -*-

import random
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from settings import AGENTS


class RotateUserAgentMiddleware(UserAgentMiddleware):
    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent
