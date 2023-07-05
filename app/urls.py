from django.contrib import admin
from django.urls import path, include
import json,os
from pathlib import Path
from django.utils.translation import gettext_lazy as _
from django.conf.urls.static import static
from django.conf import settings


def get_active_modules():
    with open('mainConfig.json', 'r') as config_file:
        config_data = json.load(config_file)

    
    active_modules = [module for module, status in config_data.items() if status == 'active']

    return active_modules

active_modules = get_active_modules()
base_directory = Path(__file__).resolve().parent.parent

urlpatterns = [
    path(_('admin/'), admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


for module in active_modules:
    if os.path.exists(os.path.join(base_directory,'molecules', module, 'config.json')):
        urlpatterns+=[path(module + '/', include('molecules.' + module + '.urls'))]
    else:
        module_path  = '/'.join(module.split('.'))
        if os.path.exists(os.path.join(base_directory,'molecules', module_path, 'config.json')):
            urlpatterns+=[path(module_path + '/', include('molecules.' + '.'.join(module.split('/')) + '.urls'))]
