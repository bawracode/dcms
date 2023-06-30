from django.shortcuts import render
from django.http import HttpResponse
import re
from django.core.exceptions import ObjectDoesNotExist
from .models import Blocks
from molecules.cms.pages.models import CustomPage
from django.template import Template, RequestContext
# render string to html
from molecules.cms.cms_logs.models import *


def find_block_ids(string):
    pattern = r"\{\{\s*block\s+id\s*=\s*['\"]?\s*(\d+)\s*['\"]?\s*\}\}"
    matches = re.findall(pattern, string)

    if matches:
        block_ids = [int(match) for match in matches]
        result_string = string

        for block_id in block_ids:
            try:
                block = Blocks.objects.get(id=block_id, status=1)
                pattern_with_spaces = r"\{\{\s*block\s+id\s*=\s*['\"]?\s*" + str(block_id) + r"\s*['\"]?\s*\}\}"
                result_string = re.sub(pattern_with_spaces, block.content, result_string)

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
    BlockLog.objects.create(user=request.user, action="block created", ip_address=request.META.get('REMOTE_ADDR'))

    return HttpResponse(rendered_template)


def render_block(request,slug_url):

    block = CustomPage.objects.get(slug=slug_url)

    block_collection = find_block_ids(block.content)

    template = Template(block_collection)
    context = RequestContext(request, {'user': request.user})
    rendered_template = template.render(context)
    BlockLog.objects.create(user=request.user, action=f"Block {block.slug}created", ip_address=request.META.get('REMOTE_ADDR'))
    
    return str(rendered_template)
