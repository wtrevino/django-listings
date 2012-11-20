# -*- coding: utf-8 -*-

from listings.models import Type, Job, JobStat, JobSearch

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


def activate_jobs(modeladmin, request, queryset):
    queryset.update(status=Job.ACTIVE)
activate_jobs.short_description = _('Activate selected jobs.')


def deactivate_jobs(modeladmin, request, queryset):
    queryset.update(status=Job.INACTIVE)
deactivate_jobs.short_description = _('Deactivate selected jobs.')


def mark_featured(modeladmin, request, queryset):
    queryset.update(featured=True)
mark_featured.short_description = _('Mark selected jobs as featured.')


class JobAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('Job Details'), {'fields': ['jobtype', 'category', 'title', \
                                    'city', 'outside_location', 'description']}),
        (_('Company Info'), {'fields': ['company', 'url', 'poster_email']}),
        (_('Admin Info'),  {'fields': ['apply_online', 'status', 'featured']}),
        (_('Owner info'),  {'fields': ['owner']}),
        (_('Sites info'),  {'fields': ['sites']}),
    ]
    list_display = ('title', 'get_location', 'get_sites', 'company', 'created_on', 'get_status_with_icon', 'featured')
    actions = [activate_jobs, deactivate_jobs, mark_featured]


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'category_order')


class TypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'ascii_name': ('name',)}


class JobStatAdmin(admin.ModelAdmin):
    readonly_fields = ['description', 'job', 'created_on', 'ip', 'stat_type']


class JobSearchAdmin(admin.ModelAdmin):
    readonly_fields = ['keywords', 'created_on']

admin.site.register(Type, TypeAdmin)
admin.site.register(Job, JobAdmin)
#admin.site.register(City, CityAdmin)
admin.site.register(JobStat, JobStatAdmin)
admin.site.register(JobSearch, JobSearchAdmin)
