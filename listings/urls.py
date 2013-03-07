# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
from listings.models import Job
from listings.conf import settings as listings_settings
from listings.feeds import LatestJobsFeed

from cities_light.models import City

if listings_settings.LISTINGS_CAPTCHA_POST == 'simple':
    from listings.forms import CaptchaJobForm
    form_class = CaptchaJobForm
else:
    from listings.forms import JobForm
    form_class = JobForm


urlpatterns = patterns('django.views.generic',

                       url(r'^$', 'list_detail.object_list',  # Index view
                       {'queryset': Job.active.order_by('-created_on').select_related(),
                       'paginate_by': listings_settings.LISTINGS_JOBS_PER_PAGE,
                       'template_name': 'listings/index.html',
                       'template_object_name': 'ad'},
                       name='listings_job_list'),

                       url(r'^' + listings_settings.LISTINGS_CITIES_URL + '/$',  # Cities view
                       'list_detail.object_list',
                       {'queryset': City.objects.all(),
                       'extra_context': {'page_type': 'cities',
                       'other_cities_total': Job.active.filter(city=None).count}},
                       name='listings_cities_list'),

                       url(r'^' + listings_settings.LISTINGS_POST_URL + '/$',  # Post new job
                       'create_update.create_object',
                       {'form_class': form_class,
                       'post_save_redirect': '../' +
                       listings_settings.LISTINGS_VERIFY_URL + '/%(id)d/%(auth)s/'},
                       name='listings_job_post'),

                       url(r'^' + listings_settings.LISTINGS_UNAVAILABLE_URL + '/$',  # Job unavailable
                       'simple.direct_to_template',
                       {'template': 'listings/unavailable.html'},
                       name='listings_job_unavailable'),

                       )


urlpatterns += patterns('',

                        url(r'^' + listings_settings.LISTINGS_VERIFY_URL +  # verify job
                        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
                        'listings.views.job_verify',
                        name='listings_job_verify'),

                        url(r'^' + listings_settings.LISTINGS_JOBS_URL + '/$',  # all jobs
                        'listings.views.jobs_category',
                        name='listings_job_list_all'),

                        url(r'^' + listings_settings.LISTINGS_JOBS_URL +  # all jobs with category
                        '/(?P<cslug>[-\w]+)/$',
                        'listings.views.jobs_category',
                        name='listings_job_list_category'),

                        url(r'^' + listings_settings.LISTINGS_JOBS_URL +  # all jobs with category and job type
                        '/(?P<cslug>[-\w]+)/(?P<tslug>[-\w]+)/$',
                        'listings.views.jobs_category',
                        name='listings_job_list_category_type'),

                        url(r'^' + listings_settings.LISTINGS_JOB_URL +  # Job detail
                        '/(?P<job_id>\d+)/(?P<ad_url>[-\w]+)/$',
                        'listings.views.job_detail',
                        name='listings_ad_detail'),

                        url(r'^' + listings_settings.LISTINGS_JOBS_IN_URL +  # Jobs in city view
                        '/(?P<city_name>[-\w]+)/$',
                        'listings.views.jobs_in_city',
                        name='listings_jobs_in_city'),

                        url(r'^' + listings_settings.LISTINGS_JOBS_IN_OTHER_CITIES_URL + '/$',  # Jobs in other cities
                        'listings.views.jobs_in_other_cities',
                        name='listings_jobs_in_other_cities'),

                        url(r'^' + listings_settings.LISTINGS_JOBS_IN_URL +  # Jobs in city+jobtype view
                        '/(?P<city_name>[-\w]+)/(?P<tslug>[-\w]+)/$',
                        'listings.views.jobs_in_city',
                        name='listings_jobs_in_city_jobtype'),

                        url(r'^' + listings_settings.LISTINGS_COMPANIES_URL + '/$',  # Companies
                        'listings.views.companies',
                        name='listings_companies'),

                        url(r'^' + listings_settings.LISTINGS_JOBS_AT_URL +  # Jobs at (company)
                        '/(?P<company_slug>[-\w]+)/$',
                        'listings.views.jobs_at',
                        name='listings_jobs_at'),

                        url(r'^' + listings_settings.LISTINGS_CONFIRM_URL +  # Job confirm
                        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
                        'listings.views.job_confirm',
                        name='listings_job_confirm'),

                        url(r'^' + listings_settings.LISTINGS_POST_URL +  # Edit job
                        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
                        'listings.views.job_edit',
                        name='listings_ad_edit'),

                        url(r'^' + listings_settings.LISTINGS_ACTIVATE_URL +  # Activate job
                        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
                        'listings.views.job_activate',
                        name='listings_ad_activate'),

                        url(r'^' + listings_settings.LISTINGS_DEACTIVATE_URL +  # Deactivate job
                        '/(?P<job_id>\d+)/(?P<auth>[-\w]+)/$',
                        'listings.views.job_deactivate',
                        name='listings_ad_deactivate'),

                        url(r'^' + listings_settings.LISTINGS_SEARCH_URL + '/$',  # Search
                        'listings.views.job_search',
                        name='listings_job_search'),

                        url(r'^rss/(?P<slug>[-\w]+)/$',  # RSS Feed
                        LatestJobsFeed(),
                        name='listings_feed'),

                        )

#Syndication feeds

urlpatterns += patterns('', url(r'^feeds/', include('listings.syndication.urls')), )
