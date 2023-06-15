from django import template
from dcms.block.models import Blocks
from django.utils.safestring import mark_safe


register = template.Library()

@register.simple_tag()
def block(id):
    try:
        block = Blocks.objects.get(id=id)
        return mark_safe(block.content)
    except Blocks.DoesNotExist:
        return ""

    
