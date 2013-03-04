# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_str, force_unicode
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags
from django import VERSION as django_version
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.conf import settings as django_settings

from listings.helpers import last_hour, getIP, strip_disallowed_tags
from listings.models.base_models import Posting
from listings.conf import settings as listings_settings

import datetime


class Type(models.Model):
    ''' The Type model, nothing special, just the name and
        slug fields. Again, the slug is slugified by the overriden
        save() method in case it's not provided.
    '''
    name = models.CharField(_('Name'), unique=True, max_length=16, blank=False)
    slug = models.SlugField(_('Slug'), unique=True, max_length=32, blank=False)
    sites = models.ManyToManyField(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        app_label = 'listings'
        verbose_name = _('Type')
        verbose_name_plural = _('Types')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Type, self).save(*args, **kwargs)


class Job(Posting):
    if django_version[:2] > (1, 2):
        category = models.ForeignKey('categories.Category', verbose_name=_('Category'), blank=False, null=True, on_delete=models.SET_NULL)
        jobtype = models.ForeignKey(Type, verbose_name=_('Job Type'), blank=False, null=True, on_delete=models.SET_NULL)
    else:
        category = models.ForeignKey('categories.Category', verbose_name=_('Category'), blank=False, null=False)
        jobtype = models.ForeignKey(Type, verbose_name=_('Job Type'), blank=False, null=False)

    company = models.CharField(_('Company'), max_length=150, blank=False)

    #TODO: Esto podria ser un atributo mejor...
    company_slug = models.SlugField(max_length=150, blank=False, editable=False)
    #url of the company
    url = models.URLField(verify_exists=False, max_length=150, blank=True)

    #url of the job post
    ad_url = models.CharField(blank=True, editable=False, max_length=32)

    apply_online = models.BooleanField(default=True, verbose_name=_('Allow online applications.'), help_text=_('If you are unchecking this, then add a description on how to apply online!'))

    class Meta:
        app_label = 'listings'
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')

    def get_location(self):
        return self.city or self.outside_location
    get_location.admin_order = 'location'
    get_location.short_description = 'Location'

    def get_application_count(self):
        return JobStat.objects.filter(job=self, stat_type='A').count()

    def get_description(self):
        return self.description_html or self.description

    def increment_view_count(self, request):  # TODO: Move to Posting
        lh = last_hour()
        ip = getIP(request)
        hits = JobStat.objects.filter(created_on__range=lh, ip=ip, stat_type='H', job=self).count()
        if hits < listings_settings.LISTINGS_MAX_VISITS_PER_HOUR:
            self.views_count = self.views_count + 1
            self.save()
            new_hit = JobStat(ip=ip, stat_type='H', job=self)
            new_hit.save()

    def clean(self):
        #making sure a job location is selected/typed in
        if self.city:
            self.outside_location = ''
        elif len(self.outside_location.strip()) > 0:
            self.city = None
        else:
            raise ValidationError(_('You must select or type a job location.'))

    def save(self, *args, **kwargs):
        #saving company slug
        self.company_slug = slugify(self.company)

        #saving job url
        self.ad_url = slugify(self.title) + \
            '-' + listings_settings.LISTINGS_AT_URL + \
            '-' + slugify(self.company)

        self.description_text = strip_tags(self.description)

        # when saving with textile
        if listings_settings.LISTINGS_MARKUP_LANGUAGE == 'textile':
            import textile
            self.description = mark_safe(
                force_unicode(
                    textile.textile(
                        smart_str(self.description))))
        # or markdown
        elif listings_settings.LISTINGS_MARKUP_LANGUAGE == 'markdown':
            import markdown
            self.description = mark_safe(
                force_unicode(
                    markdown.markdown(
                        smart_str(self.description))))

        # or wysiwyg
        elif listings_settings.LISTINGS_MARKUP_LANGUAGE == 'html':
            import django_wysiwyg
            self.description = mark_safe(
                force_unicode(
                    django_wysiwyg.clean_html(self.description)))

        # or else, disallow all markup
        else:
            self.description = self.description_text

        self.description = strip_disallowed_tags(self.description)

        super(Job, self).save(*args, **kwargs)
        current_site = Site.objects.get(pk=django_settings.SITE_ID)
        if current_site not in self.sites.all():
            self.sites.add(current_site)


class JobStat(models.Model):
    APPLICATION = 'A'
    HIT = 'H'
    SPAM = 'S'
    STAT_TYPES = (
        (APPLICATION, _('Application')),
        (HIT, _('Hit')),
        (SPAM, _('Spam')),
    )
    if django_version[:2] > (1, 2):
        job = models.ForeignKey(Job, blank=False, null=True, on_delete=models.SET_NULL)
    else:
        job = models.ForeignKey(Job)
    created_on = models.DateTimeField(default=datetime.datetime.now())
    ip = models.IPAddressField()
    stat_type = models.CharField(max_length=1, choices=STAT_TYPES)
    description = models.CharField(_('Description'), max_length=250)
    sites = models.ManyToManyField(Site)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        app_label = 'listings'
        verbose_name = _('Job Stat')
        verbose_name_plural = _('Job Stats')

    def __unicode__(self):
        return self.description

    def save(self, *args, **kwargs):
        self.description = u'%s for [%d]%s from IP: %s' % \
            (self.get_stat_type_display(), self.job.pk, self.job.title, self.ip)
        super(JobStat, self).save(*args, **kwargs)


class JobSearch(models.Model):
    keywords = models.CharField(_('Keywords'), max_length=100, blank=False)
    created_on = models.DateTimeField(_('Created on'), default=datetime.datetime.now())

    class Meta:
        app_label = 'listings'
        verbose_name = _('Search')
        verbose_name_plural = _('Searches')

    def __unicode__(self):
        return self.keywords
