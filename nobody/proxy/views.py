# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404

from controls import FetchProxy, rq_clear_proxy
from models import NobodyProxy


def get_proxies(request):
    proxies = NobodyProxy.get_all()
    output = '<br />'.join(["%s-%s" % (proxy.proxy, proxy.priority) for proxy in proxies])
    output += '<br /> %s' % len(proxies)
    return HttpResponse(output)


def get_proxy(request, pk):
    proxy = NobodyProxy.get(pk=pk)

    if proxy:
        return HttpResponse("%s-%s" % (proxy.proxy, proxy.priority))
    else:
        raise Http404("Not Found it.")


def fetch_proxy(request):
    rq_clear_proxy()

    for site in FetchProxy.PROXY_SITE:
        try:
            f = FetchProxy(*site)
            proxies = f.fetch_proxy()
            for proxy, priority in proxies.iteritems():
                f.save_proxy(proxy, priority)
        except Exception as e:
            _ = e.message
    return HttpResponse("...done.")
