import os
import json
from django.conf import settings

from django.core.management.base import BaseCommand
from django.contrib.staticfiles.finders import find


class Command(BaseCommand):
    help = 'Update JSON files with new JS and CSS file details'

    def handle(self, *args, **options):
        base_dir = settings.BASE_DIR

        molecules_path = os.path.join(base_dir,'molecules')  
        

        apps = []
        for m_folder in os.listdir(molecules_path):

            app_path = os.path.join(molecules_path, m_folder)
            a_str = m_folder + "."

            for app in os.listdir(app_path):
                files = os.path.join(app_path, app)
                f_str = a_str + app 

                for app1 in os.listdir(files):
                    if (app1 == "config.json"):
                        apps.append(f_str)

        print(apps)


      