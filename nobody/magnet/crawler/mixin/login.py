# -*- coding: utf-8 -*-

from scrapy.http import Request, FormRequest


class LoginMixin(object):
    def start_requests(self):
        meta = getattr(self, 'login_data', {})

        if 'url' not in meta:
            raise KeyError

        if hasattr(self, 'prepare_login'):
            prepare_url = meta.get('prepare_url') or meta.get('url')
            yield Request(prepare_url, meta=meta, callback=self.login)
        else:
            kwargs = {}
            self.update_kwargs(kwargs, meta)
            yield FormRequest(meta['url'], callback=self.start, **kwargs)

    def login(self, response):
        meta = response.meta
        kwargs = {}
        form_data = self.prepare_login(response)
        kwargs['formdata'] = form_data
        self.update_kwargs(kwargs, meta)
        yield FormRequest(meta['url'], callback=self.start, **kwargs)

    def update_kwargs(self, kwargs, meta):
        kwargs.update({
            'method': 'POST' if meta.get('data') else 'GET',
            'formdata': meta.get('data') or meta.get('params'),
            'headers': meta.get('headers'),
            'cookies': self.cookies(meta.get('cookie')),
        })

    @staticmethod
    def cookies(cookie):
        if isinstance(cookie, basestring):
            cookies = {}
            for _ in cookie.split(';'):
                index = _.find('=')
                cookies.update({_[:index]: _[index+1:]})
            return cookies
        elif isinstance(cookie, dict):
            return cookie
        else:
            return {}

    def start(self, response):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)
