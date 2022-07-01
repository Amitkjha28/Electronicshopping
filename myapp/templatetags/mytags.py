import datetime

from django import template

register = template.Library()

@register.simple_tag
def current_date():
    return datetime.datetime.now()
