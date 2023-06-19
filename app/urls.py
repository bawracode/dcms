from django.contrib import admin
from django.urls import path, include
import json,os
from pathlib import Path


def get_active_modules():
    with open('mainConfig.json', 'r') as config_file:
        config_data = json.load(config_file)

    
    active_modules = [module for module, status in config_data.items() if status == 'active']

    return active_modules

active_modules = get_active_modules()
base_directory = Path(__file__).resolve().parent.parent

urlpatterns = [
    path(_('admin/'), admin.site.urls),
]

for module in active_modules:
    if os.path.exists(os.path.join(base_directory,'molecules', module, 'urls.py')):
        urlpatterns+=[path(module + '/', include('molecules.' + module + '.urls'))]    

for app in os.listdir(os.path.join(base_directory,'molecules','cms')):
    urlpatterns+=[path(app + '/', include('molecules.' + 'cms' + '.' + app + '.urls'))]

