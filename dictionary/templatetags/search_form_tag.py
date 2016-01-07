import re

from django import template
from django.template import Context
from django.template.loader import render_to_string

from ..forms import SearchForm

NV_DICTIONARY_URL = 'dictionary'

if hasattr(settings, 'NV_DICTIONARY_URL'):
    if settings.NV_DICTIONARY_URL:
        NV_DICTIONARY_URL = settings.NV_DICTIONARY_URL

register = template.Library()

@register.inclusion_tag('tag-search-form.html')
def search_form_tag():
    form = SearchForm()
    return {'search_form':form, 'dictionary_url': NV_DICTIONARY_URL}
