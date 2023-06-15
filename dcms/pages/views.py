from django.shortcuts import render,HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from dcms.block.models import Blocks
from .models import CustomPage
import re

    
def index(request,slug_url):

    page_content = CustomPage.objects.get(slug=slug_url)
    print(page_content,"page_content")
    pattern = r'\{\{block id=[\'"]?(\d+)[\'"]?\}\}'
    matches = re.findall(pattern, page_content.content)
    if matches:
        block_ids = [int(match) for match in matches]
        result_string = page_content.content
        for block_id in block_ids:
                block = Blocks.objects.get(id=block_id, status=1)
                block_content = block.content
                print(result_string.find('block id='))
                print(('{{block id=' + str(block_id) + '}}'))
                result_strings = result_string.replace('{{block id=' + str(block_id) + '}}', block_content)
                print(result_strings,"block.content")
    
    return HttpResponse(result_strings)