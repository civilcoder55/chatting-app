from django import template
from datetime import datetime

register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def time(date):
    return date.strftime("%H:%M %p")