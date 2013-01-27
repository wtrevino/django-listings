# -*- coding: utf-8 -*-

from django.contrib import admin
from django.forms.widgets import ClearableFileInput
from django import forms

from listings.syndication.models import Feed


class FeedTemplateInput(ClearableFileInput):

    def render(self, name, value, attrs=None):
        def _get_template_content(value):
            return '<div style="border: 1px solid #bbb; border-radius: 10px; padding: 5px;"><code> %s </code></div>' % value.read().replace(' ', '&nbsp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br />').replace('%', '&#37;')  # i know... ugly :D
        if hasattr(value, 'read'):
            self.template_with_initial = u'%(initial_text)s: %(initial)s %(clear_template)s<br /><br /> ' + _get_template_content(value) + '   %(input_text)s: %(input)s'
        return super(FeedTemplateInput, self).render(name, value, attrs=attrs)


class FeedForm(forms.ModelForm):
    template = forms.FileField(widget=FeedTemplateInput())


class FeedAdmin(admin.ModelAdmin):
    form = FeedForm

admin.site.register(Feed, FeedAdmin)
