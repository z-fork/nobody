# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin

# from proxy import api as proxy_api

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^people/', include('people.urls')),
    # url(r'^proxy/', include('proxy.urls')),

    # api
    # url(r'^api/get_proxy', proxy_api.get_proxy, name='proxy_get_proxy'),
)

