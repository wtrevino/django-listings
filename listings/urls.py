# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from listings.models import Job, City
from listings.conf import settings as listings_settings
from listings.feeds import LatestJobsFeed

if listings_settings.LISTINGS_CAPTCHA_POST == 'simple':
    from listings.forms import CaptchaJobForm
    form_class = CaptchaJobForm
else:
    from listings.forms import JobForm
    form_class = JobForm


urlpatterns = patterns('django.views.generic',

    #An index view
    url(r'^$',
        'list_detail.object_list',
         {'queryset': Job.active.all(),
          'extra_context': {'page_type': 'index'},
          'paginate_by': listings_settings.LISTINGS_JOBS_PER_PAGE},
        name='listings_job_list'),

    #Cities view
    url(r'^' + listings_settings.LISTINGS_CITIES_URL + '/$',
        'list_detail.object_list',
         {'queryset': City.objects.all(),
          'extra_context': {'page_type': 'cities',
                    'other_cities_total': Job.active.filter(city=None).count}},
        name='listings_cities_list'),

    #post new job
    url(r'^' + listings_settings.LISTINGS_POST_URL + '/$',
        'create_update.create_object',
         {'form_class': form_class,
          'post_save_redirect': '../' +
          listings_settings.LISTINGS_VERIFY_URL + '/%(id)d/%(auth)s/'},
        name='listings_job_post'),

    #job unavailable
    url(r'^' + listings_settings.LISTINGS_UNAVAILABLE_URL + '/$',
        'simple.direct_to_template',
        {'template': 'listings/unavailable.html'},
        name='listings_job_unavailable'),
)

urlpatterns += patterns('',

    #verify job
    url(r'^' + listings_settings.LISTINGS_VERIFY_URL +
        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
        'listings.views.job_verify',
        name='listings_job_verify'),

    #all jobs
    url(r'^' + listings_settings.LISTINGS_JOBS_URL + '/$',
        'listings.views.jobs_category',
        name='listings_job_list_all'),

    #all jobs with category
    url(r'^' + listings_settings.LISTINGS_JOBS_URL +
        '/(?P<cvar_name>[-\w]+)/$',
        'listings.views.jobs_category',
        name='listings_job_list_category'),

    #all jobs with category and job type
    url(r'^' + listings_settings.LISTINGS_JOBS_URL +
        '/(?P<cvar_name>[-\w]+)/(?P<tvar_name>[-\w]+)/$',
        'listings.views.jobs_category',
        name='listings_job_list_category_type'),

    #Job detail
    url(r'^' + listings_settings.LISTINGS_JOB_URL +
        '/(?P<job_id>\d+)/(?P<joburl>[-\w]+)/$',
        'listings.views.job_detail',
        name='listings_ad_detail'),

    #Jobs in city view
    url(r'^' + listings_settings.LISTINGS_JOBS_IN_URL +
        '/(?P<city_name>[-\w]+)/$',
        'listings.views.jobs_in_city',
        name='listings_jobs_in_city'),

    #Jobs in other cities
    url(r'^' + listings_settings.LISTINGS_JOBS_IN_OTHER_CITIES_URL + '/$',
        'listings.views.jobs_in_other_cities',
        name='listings_jobs_in_other_cities'),

    #Jobs in city+jobtype view
    url(r'^' + listings_settings.LISTINGS_JOBS_IN_URL +
        '/(?P<city_name>[-\w]+)/(?P<tvar_name>[-\w]+)/$',
        'listings.views.jobs_in_city',
        name='listings_jobs_in_city_jobtype'),

    #Companies
    url(r'^' + listings_settings.LISTINGS_COMPANIES_URL + '/$',
        'listings.views.companies',
        name='listings_companies'),

    #Jobs at (company)
    url(r'^' + listings_settings.LISTINGS_JOBS_AT_URL +
        '/(?P<company_slug>[-\w]+)/$',
        'listings.views.jobs_at',
        name='listings_jobs_at'),

    #Job confirm
    url(r'^' + listings_settings.LISTINGS_CONFIRM_URL +
        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
        'listings.views.job_confirm',
        name='listings_job_confirm'),

    #Edit job
    url(r'^' + listings_settings.LISTINGS_POST_URL +
        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
        'listings.views.job_edit',
        name='listings_ad_edit'),

    #Activate job
    url(r'^' + listings_settings.LISTINGS_ACTIVATE_URL +
        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
        'listings.views.job_activate',
        name='listings_ad_activate'),

    #Deactivate job
    url(r'^' + listings_settings.LISTINGS_DEACTIVATE_URL +
        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
        'listings.views.job_deactivate',
        name='listings_ad_deactivate'),

    #Search
    url(r'^' + listings_settings.LISTINGS_SEARCH_URL + '/$',
        'listings.views.job_search',
        name='listings_job_search'),

    #Feed
    url(r'^rss/(?P<var_name>[-\w]+)/$',
        LatestJobsFeed(),
        name='listings_feed'),
)
