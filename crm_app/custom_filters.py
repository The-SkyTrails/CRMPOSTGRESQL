# custom_filters.py

from urllib.parse import urlparse

from django import template

register = template.Library()

@register.filter
def filename(value):
    """
    Extracts the filename from a given URL.
    """
    return urlparse(value).path.split('/')[-1]

