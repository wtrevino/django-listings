# -*- coding: utf-8 -*-

import re
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# General settings
LISTINGS_SITE_NAME = getattr(settings, 'LISTINGS_SITE_NAME', 'Djobberbase')
LISTINGS_SITE_SLUG = getattr(settings, 'LISTINGS_SITE_SLUG', 'djobberbase')
LISTINGS_HTML_TITLE = getattr(settings, 'LISTINGS_HTML_TITLE', 'Djobberbase :: A jobberBase clone written using the Django framework')
LISTINGS_SITE_KEYWORDS = getattr(settings, 'LISTINGS_SITE_KEYWORDS', ('job search', 'jobs', 'employment'))
LISTINGS_SITE_DESCRIPTION = getattr(settings, 'LISTINGS_SITE_DESCRIPTION', 'Djobberbase jobs.')
LISTINGS_MINUTES_BETWEEN = getattr(settings, 'LISTINGS_MINUTES_BETWEEN', 10)
LISTINGS_MAX_UPLOAD_SIZE = getattr(settings, 'LISTINGS_MAX_UPLOAD_SIZE', 3145728)
LISTINGS_FILE_UPLOADS = getattr(settings, 'LISTINGS_FILE_UPLOADS', './uploads/')
LISTINGS_JOBS_PER_PAGE = getattr(settings, 'LISTINGS_JOBS_PER_PAGE', 50)
LISTINGS_JOBS_PER_SEARCH = getattr(settings, 'LISTINGS_JOBS_PER_SEARCH', 25)
LISTINGS_MAX_VISITS_PER_HOUR = getattr(settings, 'LISTINGS_MAX_VISITS_PER_HOUR', 1)
LISTINGS_CAPTCHA_POST = getattr(settings, 'LISTINGS_CAPTCHA_POST', None)
LISTINGS_CAPTCHA_APPLICATION = getattr(settings, 'LISTINGS_CAPTCHA_APPLICATION', None)
LISTINGS_CV_EXTENSIONS = getattr(settings, 'LISTINGS_CV_EXTENSIONS', ('pdf', 'rtf', 'doc', 'docx', 'odt'))


def geturl(url_set, url, default):  # Custom URLs settings
    ''' It checks if the url is valid and not already in use, in case
        it's an invalid url then the default url is returned.
    '''
    u = getattr(settings, url, default)
    if re.match("^[a-zA-Z0-9_.-]+$", u) is not None and u not in url_set:
        url_set.append(u)
    else:
        raise ImproperlyConfigured('The url "%s" is already in use' % u)
    return u

url_set = []
LISTINGS_POST_URL = geturl(url_set, 'LISTINGS_POST_URL', 'post')
LISTINGS_VERIFY_URL = geturl(url_set, 'LISTINGS_VERIFY_URL', 'verify')
LISTINGS_CONFIRM_URL = geturl(url_set, 'LISTINGS_CONFIRM_URL', 'confirm')
LISTINGS_JOB_URL = geturl(url_set, 'LISTINGS_JOB_URL', 'job')
LISTINGS_AT_URL = geturl(url_set, 'LISTINGS_AT_URL', 'at')
LISTINGS_JOBS_URL = geturl(url_set, 'LISTINGS_JOBS_URL', 'jobs')
LISTINGS_CITIES_URL = geturl(url_set, 'LISTINGS_CITIES_URL', 'cities')
LISTINGS_COMPANIES_URL = geturl(url_set, 'LISTINGS_COMPANIES_URL', 'companies')
LISTINGS_JOBS_IN_URL = geturl(url_set, 'LISTINGS_JOBS_IN_URL', 'jobs-in')
LISTINGS_JOBS_IN_OTHER_CITIES_URL = geturl(url_set, 'LISTINGS_JOBS_IN_OTHER_CITIES_URL', 'jobs-in-other-cities')
LISTINGS_JOBS_AT_URL = geturl(url_set, 'LISTINGS_JOBS_AT_URL', 'jobs-at')
LISTINGS_ACTIVATE_URL = geturl(url_set, 'LISTINGS_ACTIVATE_URL', 'activate')
LISTINGS_DEACTIVATE_URL = geturl(url_set, 'LISTINGS_DEACTIVATE_URL', 'deactivate')
LISTINGS_SEARCH_URL = geturl(url_set, 'LISTINGS_SEARCH_URL', 'search')
LISTINGS_UNAVAILABLE_URL = geturl(url_set, 'LISTINGS_UNAVAILABLE_URL', 'job-unavailable')
LISTINGS_LOCATION_IN_URL = getattr(settings, 'LISTINGS_LOCATION_IN_URL', True)

# Mailing settings
LISTINGS_ENABLE_NEW_POST_MODERATION = getattr(settings, 'LISTINGS_ENABLE_NEW_POST_MODERATION', True)
LISTINGS_ADMIN_EMAIL = getattr(settings, 'LISTINGS_ADMIN_EMAIL', '')
LISTINGS_ADMIN_NOTIFICATIONS = getattr(settings, 'LISTINGS_ADMIN_NOTIFICATIONS', False)
LISTINGS_POSTER_NOTIFICATIONS = getattr(settings, 'LISTINGS_POSTER_NOTIFICATIONS', False)
LISTINGS_APPLICATION_NOTIFICATIONS = getattr(settings, 'LISTINGS_APPLICATION_NOTIFICATIONS', False)

LISTINGS_NEW_POST_ADMIN_SUBJECT = getattr(settings, 'LISTINGS_NEW_POST_ADMIN_SUBJECT', '[ %(site_name)s  ] New job: %(job_title)s')

LISTINGS_EDIT_POST_ADMIN_SUBJECT = getattr(settings, 'LISTINGS_EDIT_POST_ADMIN_SUBJECT', '[ %(site_name)s  ] Edited job: %(job_title)s')

LISTINGS_MAIL_PENDING_SUBJECT = getattr(settings, 'LISTINGS_MAIL_PENDING_SUBJECT', 'Your ad on %(site_name)s')

LISTINGS_MAIL_PUBLISH_SUBJECT = getattr(settings, 'LISTINGS_MAIL_PUBLISH_SUBJECT', 'Your ad on %(site_name)s was published')

LISTINGS_MAIL_APPLY_ONLINE_SUBJECT = getattr(settings, 'LISTINGS_MAIL_APPLY_ONLINE_SUBJECT', '[ %(site_name)s ] I wish to apply for %(job_title)s')


# Markup settings
LISTINGS_MARKUP_LANGUAGE = getattr(settings, 'LISTINGS_MARKUP_LANGUAGE', None)  # options: 'textile', 'markdown'
LISTINGS_ALLOWED_TAGS = getattr(settings, 'LISTINGS_ALLOWED_TAGS', ['p', 'div', 'span', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'strong', 'em', 'b', 'i', ])
