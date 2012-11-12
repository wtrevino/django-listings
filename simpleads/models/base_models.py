from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

from datetime import datetime


class TemporaryPostingsManager(CurrentSiteManager):
    def get_query_set(self):
        return super(TemporaryPostingsManager, self).get_query_set() \
                        .filter(status=self.model.TEMPORARY)


class ActivePostingsManager(CurrentSiteManager):
    def get_query_set(self):
        return super(ActivePostingsManager, self).get_query_set() \
                        .filter(status=self.model.ACTIVE)


POSTING_INACTIVE = 0
POSTING_TEMPORARY = 1
POSTING_ACTIVE = 2
POSTING_STATUS_CHOICES = (
    (POSTING_INACTIVE, _('Inactive')),
    (POSTING_TEMPORARY, _('Temporary')),
    (POSTING_ACTIVE, _('Active'))
)


class Posting(models.Model):
    ''' The basic posting model.
    '''

    class Meta:
        abstract = True
        app_label = 'simpleads'

    owner = models.ForeignKey(User, blank=True, null=True)
    title = models.CharField(verbose_name=_('Title'), max_length=100, blank=False)
    description = models.TextField(_('Description'), blank=False)
    description_html = models.TextField(editable=False)

    #city = models.ForeignKey(City, verbose_name=_('City'), null=True, blank=True)
    outside_location = models.CharField(_('Outside location'), max_length=150, blank=True)

    created_on = models.DateTimeField(_('Created on'), editable=False, \
                                        default=datetime.now())
    status = models.IntegerField(choices=POSTING_STATUS_CHOICES, default=POSTING_TEMPORARY)
    views_count = models.IntegerField(editable=False, default=0)
    auth = models.CharField(blank=True, editable=False, max_length=32)

    poster_email = models.EmailField(_('Poster email'), blank=False)
    spotlight = models.BooleanField(_('Spotlight'), default=False)
    objects = models.Manager()

    on_site = CurrentSiteManager()
    active = ActivePostingsManager()
    temporary = TemporaryPostingsManager()
    sites = models.ManyToManyField(Site)

    def get_sites(self):
        return ', '.join([site.name for site in self.sites.all()])
    get_sites.allow_tags = True
    get_sites.admin_order_field = 'sites'
    get_sites.short_description = 'Sites'
