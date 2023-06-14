from django.shortcuts import render
from django.http import HttpResponse
import re
from django.core.exceptions import ObjectDoesNotExist
from .models import Blocks
# render string to html


def find_block_ids(string):
    pattern = r'\{\{block id=[\'"]?(\d+)[\'"]?\}\}'
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

    return HttpResponse(block_collection)
