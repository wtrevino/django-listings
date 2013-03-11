# -*- coding: utf-8 -*-

from django.conf import settings

from listings.conf import settings as listings_settings
from listings.models import Type

from categories.models import Category


def general_settings(request):
    tv = {}
    tv['LISTINGS_SITE_NAME'] = listings_settings.LISTINGS_SITE_NAME
    tv['LISTINGS_SITE_SLUG'] = listings_settings.LISTINGS_SITE_SLUG
    tv['LISTINGS_HTML_TITLE'] = listings_settings.LISTINGS_HTML_TITLE
    tv['LISTINGS_SITE_KEYWORDS'] = listings_settings.LISTINGS_SITE_KEYWORDS
    tv['LISTINGS_SITE_DESCRIPTION'] = listings_settings.LISTINGS_SITE_DESCRIPTION
    #LANGUAGE_CODE = settings.LANGUAGE_CODE
    #try:
    #    LANGUAGE_CODE = LANGUAGE_CODE.split('-')[0]
    #except IndexError:
    #    LANGUAGE_CODE = 'en'
    #tv['LANGUAGE_CODE'] = LANGUAGE_CODE
    tv['markup_lang'] = getattr(listings_settings, 'LISTINGS_MARKUP_LANGUAGE', None)
    return tv


def categories_and_types(request):
    tv = {}
    tv['listings_categories'] = Category.on_site.all().order_by('order')
    tv['listings_types'] = Type.on_site.all()
    return tv
