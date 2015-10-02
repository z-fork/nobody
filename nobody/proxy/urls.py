# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from proxy import views


urlpatterns = patterns(
    '',
    url(r'^all/$', views.get_proxies, name='proxy_get_proxies'),
    url(r'^(?P<pk>[0-9]+)/$', views.get_proxy, name='proxy_get_proxy'),
    url(r'^fetch_proxy/$', views.fetch_proxy, name='proxy_fetch_proxy'),
)
