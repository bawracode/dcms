from django.shortcuts import render
from django.http import HttpResponse
import re
from django.core.exceptions import ObjectDoesNotExist
from .models import Block

def find_block_ids(string):
    pattern = r'\{\{block id=[\'"]?(\d+)[\'"]?\}\}'
    matches = re.findall(pattern, string)
    
    if matches:
        block_ids = [int(match) for match in matches]
        result_string = string
        for block_id in block_ids:
            try:
                block = Block.objects.get(id=block_id, status=True)
                result_string = result_string.replace('{{block id=' + str(block_id) + '}}', block.content)
                
                # Recursive search in the result_string
                result_string = find_block_ids(result_string)
            except ObjectDoesNotExist:
                pass
        
        return result_string
    else:
        return string





# Create your views here.
def index(request):
    text = "{{block id=4}}"
    block_id = find_block_ids(text)

    if block_id is not None:
        print(f"Found block id: {block_id}")
    else:
        print("No block id found.")

    print(block_id)
    return HttpResponse(block_id)


def dynamic_template_view(request, template_name):
    context = {}  # Additional context data to pass to the template
    
    return HttpResponse(template_name)
    return render(request, template_name, context)