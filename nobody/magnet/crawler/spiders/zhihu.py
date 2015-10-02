# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from ..mixin.login import LoginMixin


class ZhihuSipder(LoginMixin, CrawlSpider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = [
        "http://www.zhihu.com/topic"
    ]
    rules = (
        Rule(SgmlLinkExtractor(
            allow=r'http://www\.zhihu\.com/question/\d+'),
            callback='parse_page'),
    )

    login_data = {
        'prepare_url': 'http://www.zhihu.com/#signin',
        'url': 'http://www.zhihu.com/login/email',
        'cookie': {
            'cap_id': '"MDI1ODkxZjBlMTAzNDYxOTliMjk1MGE0ZjNjY2Y2NGE=|1440748116|3d8e8a1b61f1d21b53bf29f218c7ab8c4f19d8e2"',  # noqa
        },
        'data': {
            'email': '253673883@163.com',
            'password': 'qweqwe',
            'rememberme': 'y',
        }
    }

    _XSRF_XPATH = '//input[@name="_xsrf"]/@value'
    _TITLE_XPATH = '//h2[@class="zm-item-title zm-editable-content"]/text()'
    _DESCRIPTION_XPATH = '//div[@class="zm-editable-content"]/text()'

    def prepare_login(self, response):
        xsrf = response.xpath(self._XSRF_XPATH).extract()[0]
        return {
            '_xsrf': xsrf,
        }

    def parse_page(self, response):
        item = {
            'url': response.url,
            'title': response.xpath(self._TITLE_XPATH).extract(),
            'description': response.xpath(self._DESCRIPTION_XPATH).extract(),
        }
        print item


