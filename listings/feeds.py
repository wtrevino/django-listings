# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from listings.models import Job
from categories.models import Category
from listings.conf.settings import LISTINGS_SITE_NAME


class LatestJobsFeed(Feed):

    def get_object(self, request, slug):
        if slug == 'all':
            return None
        else:
            return get_object_or_404(Category, slug=slug)

    def title(self, obj=None):
        t = _(' %(site_name)s RSS Job feed') % {'site_name': LISTINGS_SITE_NAME}
        if obj:
            t += _(': %(category)s jobs') % {'site_name': obj}
        return t

    def link(self, obj=None):
        if not obj:
            return reverse('listings_job_list_all')
        else:
            return obj.get_absolute_url()

    def description(self, obj=None):
        if not obj:
            return _('Latest jobs')
        else:
            return _('Latest jobs for %(category)s ') % {'category': obj}

    def items(self, obj=None):
        jobs = Job.active.all()
        if obj:
            jobs = jobs.filter(category=obj)
        jobs = jobs.order_by('created_on')[:30]
        return jobs
