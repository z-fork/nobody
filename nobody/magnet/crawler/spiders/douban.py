# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor

from base import BaseCrawler
from magnet.crawler.contrib.store import r
from magnet.crawler import settings
from magnet.crawler.items import (
    PeopleItem,
    GroupItem,
    JoinsItem,
)


class PeopleCrawler(BaseCrawler):
    name = 'people'

    redis_key = getattr(settings, 'REDIS_KEY', 'spider:start_urls')

    allowed_domains = ['www.douban.com']

    rules = (
        Rule(LxmlLinkExtractor(
            allow=(
                r'http://www\.douban\.com/group/asshole/members$',
                r'http://www\.douban\.com/group/asshole/members\?start=\d+$',
            )),
            callback='parse_user',
            follow=True,
            process_links='process_links',
        ),
    )

    start_urls = [
        'http://www.douban.com/group/asshole/',
    ]

    _USERS_XPATH = '//li[@class=""]'
    _PAGE_XPATH = './/div[@class="name"]/a/@href'
    _NAME_XPATH = './/div[@class="name"]/a/text()'
    _LOCATION_XPATH = './/span[@class="pl"]/text()'

    def parse_user(self, response):
        users = response.xpath(self._USERS_XPATH)

        for user in users:
            page = user.xpath(self._PAGE_XPATH).extract()[0]
            name = user.xpath(self._NAME_XPATH).extract()[0]
            location = user.xpath(self._LOCATION_XPATH).extract()

            # 直接取第一页相同, 所以直接舍弃
            if response.url.endswith('start=0'):
                return

            yield PeopleItem({
                'page': page,
                'name': name,
                'location': location[0][1: -1] if location else '',
                'refer': response.url,
            })


class JoinsGroupCrawler(BaseCrawler):
    name = 'joins'

    redis_key = getattr(settings, 'REDIS_KEY', 'spider:start_urls')

    def parse(self, response):
        people = response.url[:-len('joins')]

        groups = response.xpath('//li[@class=""]')

        for group in groups:
            page = group.xpath('.//div[@class="title"]/a/@href').extract()[0]
            name = group.xpath('.//div[@class="title"]/a/@title').extract()[0]
            # (xxx)
            num = group.xpath('.//span[@class="num"]/text()').extract()[0][1:-1]

            added = r.sadd(self.name + '_group', page)
            if added:
                yield GroupItem({
                    'page': page,
                    'name': name,
                    'num': int(num),
                })

            yield JoinsItem({
                'people': people,
                'group': page
            })

