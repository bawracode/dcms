from django.core.management.templates import TemplateCommand
from django.conf import settings
from django.core.management import call_command
import os
import json
from .functions import *
import environ

env = environ.Env(
  DEBUG=(bool, False)
)

environ.Env.read_env(env_file=os.path.join(settings.BASE_DIR, ".env"))

app_folder = env("APP_FOLDER")


class Command(TemplateCommand):
    help = "Creates a Django app directory structure for the given app name, creates a templates folder, and adds a config file, and add js folder"

    def handle(self, *args, **options):

        app_name = options['name']
        
        target_folder = app_folder

        app_path = os.path.join(settings.BASE_DIR, target_folder, app_name)


        # create app
        if os.path.exists(app_path):
            pass
        else:
            os.makedirs(app_path)
        call_command('startapp', app_name, app_path)

        # Create templates folder 
        all_pps = all_apps()

        templates_path = os.path.join(settings.BASE_DIR, 'templates')
        if not os.path.exists(templates_path):
            os.makedirs(templates_path)
            all_temps = apps_templates()

        else:
            all_temps = apps_templates()

        for app in all_pps:
            if app in all_temps:
                pass
            else:
                os.makedirs(templates_path + '/' + app)


        # Create config file inside app folder
        config_file_path = os.path.join(settings.BASE_DIR, app_path,'config.json')

        
        config_data = {
                'app_name': app,
                "status": 1,
                "js":[]
            }

        with open(config_file_path, 'w') as config_file:
            json.dump(config_data, config_file, indent=4)

        

        # Create urls.py file inside app folder
        urls_file_path = os.path.join(app_path, 'urls.py')
        with open(urls_file_path, 'w') as urls_file:
            urls_file.write("""from django.urls import path
from . import views
from django.urls import path

app_name = '{0}'

urlpatterns = [
    #path('', views.index, name='index page'),
]
""".format(app_name))
        
        
        # change apps.py file
        apps_file_path = os.path.join(app_path, 'apps.py')

        app_module = f"{target_folder}.{app_name}"

        with open(apps_file_path, "r") as apps_file:
            content = apps_file.read()

        content = content.replace(f"{app_name}", f"{app_module}")
        
        with open(apps_file_path, 'w') as apps_file:
            apps_file.write(content)
            

        # add folder in static/js folder
        if not os.path.exists(os.path.join(settings.BASE_DIR, 'static')):
            os.makedirs(os.path.join(settings.BASE_DIR, 'static'))

        if not os.path.exists(os.path.join(settings.BASE_DIR, 'static', 'js')):
            os.makedirs(os.path.join(settings.BASE_DIR, 'static', 'js'))

        if not os.path.exists(os.path.join(settings.BASE_DIR, 'static', 'js',"admin")):
            os.makedirs(os.path.join(settings.BASE_DIR, 'static', 'js',"admin"))

        if not os.path.exists(os.path.join(settings.BASE_DIR, 'static', 'js',"nucleus")):
            os.makedirs(os.path.join(settings.BASE_DIR, 'static', 'js',"admin","nucleus"))

        if not os.path.exists(os.path.join(settings.BASE_DIR, 'static', 'js', app_name)):
            os.makedirs(os.path.join(settings.BASE_DIR, 'static', 'js', app_name))
        


