#-*- coding: utf-8 -*-
"""
Django urls.

"""
from django.conf.urls import patterns, url


urlpatterns = patterns('activity_feed.views',
    url(r'^$', 'activities'),
    url(r'^page/(?P<page>\d+)/$', 'activities'),

    url(r'^creator/(?P<creator>\d+)/$', 'activities'),
    url(r'^creator/(?P<creator>\d+)/page/(?P<page>\d+)/$', 'activities'),

    url(r'^target/(?P<target>\d+)/$', 'activities'),
    url(r'^target/(?P<target>\d+)/page/(?P<page>\d+)/$', 'activities'),

    url(r'^creator/(?P<creator>\d+)/target/(?P<target>\d+)/$',
        'activities'),
    url(r'^creator/(?P<creator>\d+)/target/(?P<target>\d+)/page/(?P<page>\d+)/$',
        'activities'),

    url(r'^new/$', 'create_activity'),

    url(r'^filter/$', 'filter_activities'),
)
