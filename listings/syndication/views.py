# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import Context

from listings.syndication.models import Feed
from listings.models import Job


def display_feed(request, feed_url):
    feed = get_object_or_404(Feed, feed_url=feed_url)
    ads = Job.active.all()
    template = feed.get_template()
    context = Context({'ads': ads})
    return HttpResponse(template.render(context), content_type=feed.content_type)
