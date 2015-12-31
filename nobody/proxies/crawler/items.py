# -*- coding: utf-8 -*-

import scrapy


class RedisItem(scrapy.Item):
    proxy = scrapy.Field()
    priority = scrapy.Field()
