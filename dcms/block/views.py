from django.shortcuts import render
from django.http import HttpResponse
import re
from django.core.exceptions import ObjectDoesNotExist

from .models import Blocks
from django.template import Template, RequestContext
# render string to html
from dcms.cms_logs.models import *


def find_block_ids(string):
    pattern = r'\{\{\s*block\s+id=[\'"]?\s*(\s\d+\s)\s*[\'"]?\s*\}\}'

    matches = re.findall(pattern, string)
    
    if matches:
        block_ids = [int(match) for match in matches]
        result_string = string
        for block_id in block_ids:
            try:
                block = Blocks.objects.get(id=block_id, status=1)
                result_string = result_string.replace('{{block id=' + str(block_id) + '}}', block.content)
                
                # Recursive search in the result_string
                result_string = find_block_ids(result_string)
            except ObjectDoesNotExist:
                pass
        
        return result_string
    else:
        return string


# Create your views here.
def index(request,slug_url):

    block = Blocks.objects.get(slug=slug_url)

    block_collection = find_block_ids(block.content)


    template = Template(block_collection)
    context = RequestContext(request, {'user': request.user})
    rendered_template = template.render(context)
    PageLog.objects.create(user=request.user, action="Page created", ip_address=request.META.get('REMOTE_ADDR'))

    return HttpResponse(rendered_template)
