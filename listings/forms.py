# -*- coding: utf-8 -*-


from listings.models import Job, Type, JobStat
from listings.conf import settings as listings_settings
from listings import GEO_LEVEL_COUNTRY

from django.utils.safestring import mark_safe
from django import forms
from django.utils.translation import ugettext_lazy as _

from categories.models import Category

from datetime import datetime, timedelta


class HorizRadioRenderer(forms.RadioSelect.renderer):
    """ this overrides widget method to put radio buttons horizontally
        instead of vertically.
    """
    def render(self):
        """Outputs radios"""
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ('category', 'jobtype', 'title', 'description', 'company', 'city', 'outside_location', 'url', 'poster_email', 'apply_online')
        widgets = {
            'jobtype': forms.Select(attrs={'class': 'span12'}),
            'title': forms.TextInput(attrs={'class': 'span12'}),
            'description': forms.Textarea(attrs={'class': 'span12'}),
            'city': forms.Select(attrs={'class': 'span12'}),
            'outside_location': forms.TextInput(attrs={'class': 'span12'}),
            'company': forms.TextInput(attrs={'class': 'span12'}),
            'url': forms.TextInput(attrs={'class': 'span12'}),
            'poster_email': forms.TextInput(attrs={'class': 'span12'}),
            'category': forms.Select(attrs={'class': 'span12'}),
        }

    #if settings.LISTINGS_GEO_LEVEL == GEO_LEVEL_COUNTRY:
    #    region = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)
        city = self.fields['city']
        choices = [('', '---------'), ]
        choices.extend([(_city.pk, unicode(_city.name)) for _city in city.queryset.all()])
        self.fields['city'].choices = choices


class CaptchaJobForm(JobForm):
    if listings_settings.LISTINGS_CAPTCHA_POST == "simple":
        from captcha.fields import CaptchaField
        captcha = CaptchaField()
    else:
        pass


class ApplicationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.applicant_data = kwargs.pop('applicant_data', None)
        super(ApplicationForm, self).__init__(*args, **kwargs)
    apply_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'apply_name', 'class': 'span5'}))
    apply_email = forms.EmailField(max_length=50, widget=forms.TextInput(attrs={'id': 'apply_email', 'class': 'span5'}))
    apply_msg = forms.CharField(widget=forms.Textarea(attrs={'id': 'apply_msg', 'class': 'span12'}))
    apply_cv = forms.FileField(required=False)

    if listings_settings.LISTINGS_CAPTCHA_APPLICATION == "simple":
        from captcha.fields import CaptchaField
        captcha = CaptchaField()

    def clean(self):
        cleaned_data = self.cleaned_data
        ip = self.applicant_data['ip']
        mb = self.applicant_data['mb']
        previous_applications = JobStat.objects.filter(created_on__range=mb, ip=ip, stat_type='A')
        m = previous_applications.count()
        if m > 0:
            #Getting how many minutes until user can apply again
            d1 = previous_applications.latest('created_on').created_on + timedelta(minutes=listings_settings.LISTINGS_MINUTES_BETWEEN)
            d2 = datetime.now()
            remaining = d1 - d2
            remaining = remaining.seconds / 60
            raise forms.ValidationError(_('You need to wait %(remaining)s more minute(s) before you can apply for a job again.') % {'remaining': remaining + 1})

        if cleaned_data['apply_cv']:
            #checking if cv extension is permitted
            extension = cleaned_data['apply_cv'].name.lower().split('.')[-1]
            if extension not in listings_settings.LISTINGS_CV_EXTENSIONS:
                raise forms.ValidationError(_('Your resume/CV has an invalid extension.'))
            #checking cv size does not exceed the permitted one
            permitted_size = listings_settings.LISTINGS_MAX_UPLOAD_SIZE
            if cleaned_data['apply_cv']._size > permitted_size:
                raise forms.ValidationError(_('Your resume/CV must not exceed the file size limit. (%(size)sMB)') % {'size': (permitted_size / 1024) / 1024})

        return cleaned_data
