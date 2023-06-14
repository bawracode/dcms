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
from django.urls import path,include

from django.conf import settings
import json
import os
import environ
from django.conf.urls.static import static

env = environ.Env(
  DEBUG=(bool, False)
)

environ.Env.read_env(env_file=os.path.join(settings.BASE_DIR, ".env"))

app_folder = env("APP_FOLDER")

#config file import and return path url
def return_path_url():
    with open(settings.BASE_DIR.joinpath("main_config.json")) as f:
        temp_file = json.loads(f.read())
            

    temp_str = """path("{0}/",include("{1}.{0}.urls")),"""

    online_url = [key for key in temp_file.keys() if temp_file[key]==1]

    molecular_apps = [eval(temp_str.format(app,app_folder)) for app in online_url]

    return molecular_apps


urlpatterns = [
    path("admin/", admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

for i in return_path_url():
    urlpatterns.append(i[0])
