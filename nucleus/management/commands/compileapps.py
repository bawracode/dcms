from django.core.management.base import BaseCommand
from django.conf import settings
import os, json
from nucleus.management.compilation import *
from pathlib import Path

def compile_apps(folder_name, file_path,BASE_DIR):
    appFolders = os.path.join(BASE_DIR ,folder_name)

        # Fetch app names from the molecules folder
    app_names = []
    for folders in os.listdir(appFolders):
        app_path = os.path.join(appFolders, folders)
        if not os.path.exists(os.path.join(appFolders, folders,'config.json')):                    
            for app in os.listdir(app_path):
                if os.path.exists(os.path.join(app_path, app,'config.json')):
                    app_names.append(folder_name+"."+os.path.basename(app_path)+"."+app) 
        else:
            app_names.append(folder_name+"."+os.path.basename(app_path))
   
    # Write the app names to dynamic_apps_list.txt
    with open(file_path, 'a') as file:
        file.writelines('\n'.join(app_names))
        file.write('\n')
    base_directory = settings.BASE_DIR

    molecules_directory = os.path.join(base_directory, 'molecules')

    modul_list = []
# append_modules function is used to append the modules to the list
    def append_modules(directory, modul_list):
        for foldername in os.listdir(directory):
            folder_path = os.path.join(directory, foldername)
            config_path = os.path.join(folder_path, 'config.json')

            if os.path.isfile(config_path):
                modul_list.append(foldername)
                modul_list.append('active')
            elif os.path.isdir(folder_path):
                for app in os.listdir(folder_path):
                    if os.path.isfile(os.path.join(folder_path, app, 'config.json')):
                        modul_list.append(foldername + '.' + app)
                        modul_list.append('active')
    append_modules(molecules_directory, modul_list)
# from list to mainConfig.json
    dictionary = {}
    for i in range(0, len(modul_list), 2):
        key = modul_list[i]                                                                                                                                                                                                                             
        value = modul_list[i + 1]
        dictionary[key] = value
    
    with open(os.path.join(base_directory,'mainConfig.json'), 'w') as config_file:
            json.dump(dictionary, config_file, indent=4)

class Command(BaseCommand):

    compilation = Compilation()
    help = 'Add all apps to compiled file'

    def handle(self, *args, **options):
        # Get the path of the directory containing the settings.py file
        BASE_DIR = settings.BASE_DIR
        file_name = os.path.join(BASE_DIR,'nucleus','management')

        # Get the path of dynamic_apps_list.txt
        file_path = os.path.join(self.compilation.compiled_dir, self.compilation.apps_file)

        # Define the folder name where apps are located
        folder_name = ['molecules','nucleus']
        # for folder in folder_name:
        with open(file_path, 'w') as file:
            file.write('')    
        for folder in folder_name:
            compile_apps(folder,file_path,BASE_DIR)
        

        self.stdout.write(self.style.SUCCESS(f'Successfully added apps to compiled file and mainConfig.json'))



def append_module_configs_to_root_config(folder_path, root_config):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            # Recursively traverse subdirectories
            append_module_configs_to_root_config(item_path, root_config)
        elif item == "app_config.json":
            # Found app_config.json file, append its content to root_config
            with open(item_path, "r") as f:
                app_config = json.load(f)
                for obj in app_config:
                    
                    root_config.append(obj)
                # print(app_config)

def main():
    config_compile = Compilation_config()
    compile_path = os.path.join(config_compile.compiled_dir, config_compile.config_file)
    root_config = []  # Root config to store appended JSON content
    molecules_folder = os.path.join(settings.BASE_DIR, "molecules")

    append_module_configs_to_root_config(molecules_folder, root_config)

    # Write the root config to the root_config.json file
    root_config_file = compile_path
    with open(root_config_file, "w") as f:
        json.dump(root_config, f, indent=4)

# Call the main function
main()