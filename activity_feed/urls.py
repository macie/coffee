# -*- coding: utf-8 -*-
"""
Django urls.

"""
from django.conf.urls import patterns, url


urlpatterns = patterns('activity_feed.views',
    url(r'^$', 'activities',
        {'creator': None,
         'target': None,
         'page': None}),
    url(r'^page/(?P<page>\d+)/$', 'activities',
        {'creator': None,
         'target': None}),

    url(r'^creator/(?P<creator>\d+)/$', 'activities',
        {'target': None,
         'page': None},
        name='creator_filter'),
    url(r'^creator/(?P<creator>\d+)/page/(?P<page>\d+)/$', 'activities',
        {'target': None}),

    url(r'^target/(?P<target>\d+)/$', 'activities',
        {'creator': None,
         'page': None},
        name='target_filter'),
    url(r'^target/(?P<target>\d+)/page/(?P<page>\d+)/$', 'activities',
        {'creator': None}),

    url(r'^creator/(?P<creator>\d+)/target/(?P<target>\d+)/$', 'activities',
        {'page': None}),
    url(r'^creator/(?P<creator>\d+)/target/(?P<target>\d+)/page/(?P<page>\d+)/$',
        'activities'),

    url(r'^new/$', 'create_activity'),

    url(r'^filter/$', 'filter_activities'),
)
