# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from people import views


urlpatterns = patterns(
    '',
    url(r'^all/$', views.get_peoples, name='people_get_peoples'),
    url(r'^(?P<pk>[0-9]+)/$', views.get_people, name='people_get_people'),
    # url(r'^analysis/kmeans/$', views.analysis_people_by_kmeans, name='people_analysis_kmeans')
)

