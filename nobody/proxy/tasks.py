# -*- coding: utf-8 -*-

from nobody.libs.mq import mq
# from nobody.libs.store import r

from proxy.proxy import FetchProxy


@mq.task
def fetch_proxy_task():
    # FetchProxy.test_unavailable_proxy()

    for url in FetchProxy.PROXY_SITE:
        try:
            f = FetchProxy(url)
            proxies = f.fetch_proxy()
            # f.save_proxy(proxies)
        except Exception as e:
            _ = e.message
