# -*- coding: utf-8 -*-

from listings.conf import settings
from listings.models import Job, Type

def general_settings(request):
    tv = {}
    tv['LISTINGS_SITE_NAME'] = settings.LISTINGS_SITE_NAME
    tv['LISTINGS_HTML_TITLE'] = settings.LISTINGS_HTML_TITLE 
    tv['LISTINGS_SITE_KEYWORDS'] = settings.LISTINGS_SITE_KEYWORDS
    tv['LISTINGS_SITE_DESCRIPTION'] = settings.LISTINGS_SITE_DESCRIPTION
    return tv

def categories_and_types(request):
    tv = {}
    tv['listings_categories'] = Category.on_site.all().order_by('category_order')
    tv['listings_types'] = Type.on_site.all()
    
