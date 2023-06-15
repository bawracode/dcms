from django.shortcuts import render,HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from molecules.cms.block.models import Blocks
from .models import CustomPage
import re
from molecules.cms.pages.models import *
from molecules.cms.cms_logs.models import *

from molecules.cms.block.views import render_block

    
def index(request,slug_url):

    result_strings = render_block(request,slug_url)
    PageLog.objects.create(user=request.user, action="Page created", ip_address=request.META.get('REMOTE_ADDR'))
    return HttpResponse(result_strings)