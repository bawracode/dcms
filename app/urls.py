import json,os
from pathlib import Path
from django.utils.translation import gettext_lazy as _
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import path ,include
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic.base import RedirectView as Redirectview



def get_active_modules():
    with open('mainConfig.json', 'r') as config_file:
        config_data = json.load(config_file)

    
    active_modules = [module for module, status in config_data.items() if status == 'active']

    return active_modules

active_modules = get_active_modules()
base_directory = settings.BASE_DIR

urlpatterns = [
    path('admin/', admin.site.urls),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
     


for module in active_modules:
    module_path  = '/'.join(module.split('.'))
    if os.path.exists(os.path.join(base_directory, module_path, 'config.json')):
        urlpatterns+=[path('/'.join(module.split('.')[1:]) + '/', include('.'.join(module.split('/')) + '.urls'))]
