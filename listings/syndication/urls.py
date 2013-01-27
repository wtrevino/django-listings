# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *


urlpatterns = patterns('listings.syndication.views',

    url(r'^(?P<feed_url>[-\w]+)/$',
        'display_feed',
        name='listings_display_feed'),

)
