from django import template
import os

register = template.Library()


@register.filter
def filename(value):
    return os.path.basename(value)



@register.filter
def is_pdf(file):
    return file.name.lower().endswith('.pdf')