import shutil
from django.core.management.templates import TemplateCommand
import os
import json
from pathlib import Path
from django.conf import settings

Json_list = []
class Command(TemplateCommand):
    help = "My custom startapp command."
    
    def handle(self, *args, **options):
        app_name = options['name']

        # root directory
        base_directory = settings.BASE_DIR

        # make dirs for app
        target = os.path.join(base_directory, 'molecules' , app_name)
        


        self.stdout.write(f"Creating app '{app_name}' in '{target}'...")

        os.makedirs(target, exist_ok=True)

        super().handle('app', app_name=app_name, target=target, **options)

        
        
        # update the apps file
        apps_file_path = os.path.join(target, 'apps.py')
        with open(apps_file_path, 'r') as apps_file:
            lines = apps_file.readlines()

        lines[-1] = lines[-1].replace(f'name = "{app_name}"',f'name = "molecules.{app_name}"')
        
        with open(apps_file_path, 'w') as apps_file:
            apps_file.writelines(lines)

        # create config json file for apps
        os.system(f"touch {target}/config.json")

        app_config_data = {
            'app_name': app_name,
            'path': target,
            'status': 'active',
            'jsfiles': []
        }



        # create config urls file for apps
        os.system(f"touch {target}/urls.py")

        config_file_path = os.path.join(target, f'config.json')
        urls_file_path = os.path.join(target, 'urls.py')
        apps_file_path = os.path.join(target, 'apps.py')

        # dumps the json config data
        with open(config_file_path, 'w') as config_file:
            json.dump(app_config_data, config_file, indent=4)

        # update the urls file
        with open(urls_file_path, 'w') as urls_file:
            urls_file.write(f'''from django.urls import path,include\nfrom molecules.{app_name} import views\n\n
\nurlpatterns = [\n \n]\n''')
        
        # check if all directory present if not then it build
        os.chdir(base_directory)
        if os.path.exists('static'):
            os.chdir('static')
            print(os.getcwd())
        else:
            os.system(f"mkdir static")
            os.chdir('static')

        if os.path.exists('js'):
            os.chdir('js')
        else:
            os.system(f"mkdir js")
            os.chdir('js')

        if os.path.exists('admin'):
            os.chdir('admin')
        else:
            os.system(f"mkdir admin")
            os.chdir('admin')
        if os.path.exists('nucleus'):
            os.chdir('nucleus')
        else:
            os.system(f"mkdir nucleus")
            os.chdir('nucleus')
        os.system(f"mkdir {app_name}")

        molecules_dir = [name for name in os.listdir(os.path.join(base_directory,'molecules')) if os.path.isdir(os.path.join(os.path.join(base_directory,'molecules'), name))]
        templates_dir = [name for name in os.listdir(os.path.join(base_directory,'static/js/admin/nucleus')) if os.path.isdir(os.path.join(os.path.join(base_directory,'static/js/admin/nucleus'), name))]

        # find app that not present in molecules folder and missing directory deleted
        missing_dirs = set(templates_dir) - set(molecules_dir)
        for dir_name in missing_dirs:
            os.rmdir(dir_name)
            print(f"Deleted directory: {dir_name}")

        # update main config file  
        modul_list = []
        for foldername in os.listdir(os.path.join(base_directory,'molecules')):
            modul_list.append(foldername)
            modul_list.append('active')

        dictionary = {}
        for i in range(0, len(modul_list), 2):
            key = modul_list[i]                                                                                                                                                                                                                             
            value = modul_list[i + 1]
            dictionary[key] = value
        
        with open(os.path.join(base_directory,'mainConfig.json'), 'w') as config_file:
             json.dump(dictionary, config_file, indent=4)

        self.stdout.write(self.style.SUCCESS(f"App '{app_name}' created successfully in '{target}'."))
