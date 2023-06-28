import os
import json
from django.conf import settings
from pathlib import Path
from django.core.management.base import BaseCommand
from django.contrib.staticfiles.finders import find


class Command(BaseCommand):
    help = 'Update JSON files with new JS and CSS file details'

    def handle(self, *args, **options):
        base_dir = settings.BASE_DIR
        def get_file_extension(file_path):
             _, extension = os.path.splitext(file_path)
             return extension

        
        template_folder = os.path.join(base_dir,'static')  # Replace with the actual path to your templates folder
        def append_module_configs_to_root_config(folder_path):
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isdir(item_path):
                    # Recursively traverse subdirectories
                    append_module_configs_to_root_config(item_path)
                elif get_file_extension(item) in ['.js','.css']:
                    self.update_json_files(os.path.dirname(item_path))

        append_module_configs_to_root_config(template_folder)
        

        self.stdout.write(self.style.SUCCESS('JSON files updated successfully!'))

    def update_json_files(self, app_path):
        base_dir = settings.BASE_DIR
        molecules_folder = os.path.join(base_dir,'molecules')
        for root, dirs, files in os.walk(app_path):
            for file in files:
                file_extension = os.path.splitext(file)[1][1:]  # Get the file extension
                if file_extension in ['js','css']:
                    module_name = os.path.basename(root)
                    file_path = os.path.join(root, file)
                    json_file_path = os.path.join(molecules_folder,module_name, 'config.json')
                    with open(json_file_path, 'r+') as json_file:
                        data = json.load(json_file)
                        src = os.path.join(app_path, file)
                        defer = True
                    

                        def get_file_extension(file_path):
                            _, extension = os.path.splitext(file_path)
                            return extension

                        # Example usage
                        file_path = src
                        extension = get_file_extension(file_path)
                        
                        if extension == '.js':
                        # Check if the file details already exist in the JSON data
                            if not any(entry['src'] == src and entry['defer'] == defer for entry in data['jsfiles']):
                                
                                data['jsfiles'].append({
                                    'src': src,
                                    'defer': defer
                                })
                        elif extension == '.css':
                            if not any(entry['src'] == src for entry in data['cssfiles']):
                                data['cssfiles'].append({
                                    'src': src,
                                    'defer': defer

                                })

                        json_file.seek(0)
                        json.dump(data, json_file, indent=4)
                        json_file.truncate()
                 