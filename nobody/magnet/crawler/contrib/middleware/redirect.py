# -*- coding: utf-8 -*-

import re
from urllib import urlencode
from urlparse import urljoin

import requests
from scrapy import log
from scrapy.contrib.downloadermiddleware.redirect import RedirectMiddleware

from captcha.captcha import Captcha


class CaptchaRedirectMiddleware(RedirectMiddleware):

    _MAX_RETRY_PROCESS = 5

    _CAPTCHA_PATTERN = r'"(http://www\.douban\.com/misc/captcha\?id=(.*?))" alt'
    _ORIGINAL_URL_PATTERN = r'type="hidden" name="original-url" value="(.*?)"'

    def process_response(self, request, response, spider):
        if response.status in [302, 403]:
            if 'Location' in response.headers:
                redirected_url = urljoin(request.url, response.headers['location'])
            else:
                redirected_url = request.url

            if redirected_url.startswith('http://www.douban.com/misc/sorry'):
                data = self.process_data(redirected_url)

                if data:
                    query_str = urlencode(data, doseq=1)

                    redirected = request.replace(url=redirected_url, method='POST', body=query_str)
                    redirected.headers.setdefault('Content-Type', 'application/x-www-form-urlencoded')
                    return self._redirect(redirected, request, spider, response.status)

        return super(CaptchaRedirectMiddleware, self).process_response(request, response, spider)

    def process_data(self, url):
        max_retry = self._MAX_RETRY_PROCESS
        data = {}

        while max_retry:
            data = self._process_data(url)

            if data:
                log.msg(message="%s%s%s%s" % ('|' * 5, data['captcha-id'], data['captcha-solution'], '|' * 5),
                        level=log.DEBUG)

                if data['captcha-solution']:
                    break

            max_retry -= 1

        return data

    def _process_data(self, url):
        r = requests.get(url)
        if r.status_code == 403:
            content = r.content
            try:
                img_url, img_code = re.search(self._CAPTCHA_PATTERN, content).groups()
                r = requests.get(img_url)
                if r.status_code == 200:
                    c = Captcha(content=r.content)
                    # TODO img_str 判断是否为正确单词?
                    img_str = c.to_string()

                    original_url = re.search(self._ORIGINAL_URL_PATTERN, content).group(1)

                    return {
                        'captcha-solution': img_str,
                        'captcha-id': img_code,
                        'original-url': original_url
                    }
            except AttributeError as e:
                log.msg(format="Gave up request at _process_data: %(reason)s",
                        level=log.DEBUG, reason=e.message)
