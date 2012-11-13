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

    def __unicode__(self):
        return self.title

    def get_sites(self):
        return ', '.join([site.name for site in self.sites.all()])
    get_sites.allow_tags = True
    get_sites.admin_order_field = 'sites'
    get_sites.short_description = 'Sites'

    def is_active(self):
        return self.status == self.ACTIVE

    def is_temporary(self):
        return self.status == self.TEMPORARY

    def get_status_with_icon(self):
        from django.conf import settings

        image = {
            self.ACTIVE: 'icon-yes.gif',
            self.TEMPORARY: 'icon-unknown.gif',
            self.INACTIVE: 'icon-no.gif',
        }[self.status]

        try:
            # Django 1.2
            admin_media = settings.ADMIN_MEDIA_PREFIX
            icon = '<img src="%(admin_media)simg/admin/%(image)s" alt="%(status)s" /> %(status)s'

        except AttributeError:
            # Django 1.3+
            admin_media = settings.STATIC_URL
            icon = '<img src="%(admin_media)sadmin/img/%(image)s" alt="%(status)s" /> %(status)s'

        else:
            admin_media = ''
            icon = '%(status)s'

        return icon % {'admin_media': admin_media,
                       'image': image,
                       'status': unicode(self.JOB_STATUS_CHOICES[self.status][1])}
    get_status_with_icon.allow_tags = True
    get_status_with_icon.admin_order_field = 'status'
    get_status_with_icon.short_description = 'Status'

    def activate(self):
        self.status = self.ACTIVE
        self.save()

    def deactivate(self):
        self.status = self.INACTIVE
        self.save()

    def email_published_before(self):
        return Job.active.exclude(pk=self.id) \
                          .filter(poster_email=self.poster_email).count() > 0