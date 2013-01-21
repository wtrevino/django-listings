# -*- coding: utf-8 -*-

from django.contrib import admin
from django.forms.widgets import ClearableFileInput
from django import forms

from listings.syndication.models import Feed, FeedType


class FeedTemplateInput(ClearableFileInput):

    def render(self, name, value, attrs=None):
        def _get_template_content(value):
            return '<div style="border: 1px solid #bbb; border-radius: 10px; padding: 5px;"><code> %s </code></div>' % value.read().replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br />')  # i know... ugly :D
        self.template_with_initial = u'%(initial_text)s: %(initial)s %(clear_template)s <br /><br /> ' + _get_template_content(value) + ' <br />%(input_text)s: %(input)s'
        return super(FeedTemplateInput, self).render(name, value, attrs=None)


class FeedTypeForm(forms.ModelForm):
    template = forms.FileField(widget=FeedTemplateInput())


class FeedTypeAdmin(admin.ModelAdmin):
    form = FeedTypeForm


class FeedAdmin(admin.ModelAdmin):
    pass

admin.site.register(FeedType, FeedTypeAdmin)
admin.site.register(Feed, FeedAdmin)
