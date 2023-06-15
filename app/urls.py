"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import json,os


def get_active_modules():
    with open('mainConfig.json', 'r') as config_file:
        config_data = json.load(config_file)

    
    active_modules = [module for module, status in config_data.items() if status == 'active']

    return active_modules

active_modules = get_active_modules()

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('pages/', include('molecules.cms.pages.urls')),
    # path('blocks/', include('molecules.cms.block.urls')),
]
for module in active_modules:
    if module != 'cms':
        urlpatterns.append(path(module + '/', include('molecules.' + module + '.urls')))
    else:
        pass
