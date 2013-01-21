# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.sites.models import Site

upload_to = lambda instance, filename: '/'.join(['feeds', instance.name.lower(), filename])


def validate_file_extension(value):
    extension = value.name.split('.')[-1]
    if extension not in ('tpl', 'htm', 'html'):
        raise ValidationError(_('File extension not permitted.'))


class FeedType(models.Model):
    name = models.CharField(_('Name'), unique=True, max_length=100, blank=False)
    template = models.FileField(upload_to=upload_to, validators=[validate_file_extension, ])
    content_type = models.CharField(_('Content type'), max_length=100, blank=False, default='application/xml')

    def __unicode__(self):
        return self.name


class Feed(models.Model):
    site = models.ManyToManyField(Site)
    feed_type = models.ForeignKey(FeedType)
