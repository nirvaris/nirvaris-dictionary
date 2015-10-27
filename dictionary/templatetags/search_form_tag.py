import re

from django import template
from django.template import Context
from django.template.loader import render_to_string

from ..forms import SearchForm

register = template.Library()

@register.inclusion_tag('search-form.html')
def search_form_tag():
    form = SearchForm()
    return {'search_form':form}