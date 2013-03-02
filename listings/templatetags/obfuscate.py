# -*- coding: utf-8 -*-

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags

from bs4 import BeautifulSoup

import re

from rendertext import render

EMAIL_PATTERN = re.compile("[-a-zA-Z0-9._+]+@[-a-zA-Z0-9_]+.[a-zA-Z0-9_.]+")


register = template.Library()


def get_strings(string):
    return re.findall(EMAIL_PATTERN, string)


@register.filter()
@stringfilter
def obfuscate(value):

    # remove all anchors
    soup = BeautifulSoup(value, 'html.parser')
    for anchor in soup.findAll('a'):
        anchor.replaceWith(anchor.string)
    value = soup.prettify()

    # find all email strings
    _value = strip_tags(value)
    word_list = _value.split()
    email_strings = []
    for word in word_list:
        found_strings = get_strings(word)
        for found_string in found_strings:
            if found_string not in email_strings:
                email_strings.append(found_string)

    # replace email strings with its generated image
    for string in email_strings:
        rendered = render(string, 'verdana')
        value = value.replace(string, '<img src="/%s" width="%s" height="%s" style="position: relative; top: 2px;" />' % (rendered[0], rendered[1], rendered[2]))

    return mark_safe(value)
