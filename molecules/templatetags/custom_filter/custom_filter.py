from django import template

register = template.Library()

@register.filter
def assign_value(cl, column_name):
    cl.list_display = column_name
    return cl