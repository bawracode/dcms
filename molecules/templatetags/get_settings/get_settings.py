from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def get_list_choices():
    return getattr(settings, 'LIST_PER_CHOICES', [])
