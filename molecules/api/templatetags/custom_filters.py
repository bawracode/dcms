from django import template

register = template.Library()

@register.filter
def defaultsort(value):
    return value
