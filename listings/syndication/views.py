# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from django.template import Context

from django.contrib.sites.models import Site
from listings.syndication.models import Feed


def display_feed(request, feed_url):
    site = Site.objects.get_current()
    try:
        feed = site.feed_set.get(feed_url=feed_url)
    except Feed.DoesNotExist:
        raise Http404
    template = feed.get_template()
    context = Context({'ads': feed.ads.model.active.all()})
    return HttpResponse(template.render(context), content_type=feed.content_type)
