from django.shortcuts import HttpResponse
from molecules.cms.block.views import render_block

    
def index(request,slug_url):

    result_strings = render_block(request,slug_url)
    return HttpResponse(result_strings)