import os
import json
from django.conf import settings

from django.core.management.base import BaseCommand
from django.contrib.staticfiles.finders import find


class Command(BaseCommand):
    help = 'Update JSON files with new JS and CSS file details'

    def handle(self, *args, **options):
        base_dir = settings.BASE_DIR

        template_folder = os.path.join(base_dir,'static/js/admin/nucleus')  # Replace with the actual path to your templates folder

        for app_folder in os.listdir(template_folder):
            app_path = os.path.join(template_folder, app_folder)
            if os.path.isdir(app_path):
                self.update_json_files(app_path)

        self.stdout.write(self.style.SUCCESS('JSON files updated successfully!'))

    def update_json_files(self, app_path):
        base_dir = settings.BASE_DIR
        molecules_folder = os.path.join(base_dir,'molecules')
        for root, dirs, files in os.walk(app_path):
            for file in files:
                file_extension = os.path.splitext(file)[1][1:]  # Get the file extension
                if file_extension in ['js']:
                    module_name = os.path.basename(root)
                    file_path = os.path.join(root, file)
                    json_file_path = os.path.join(molecules_folder,module_name, f'{module_name}.json')
                    print(json_file_path)
                    with open(json_file_path, 'r+') as json_file:
                        data = json.load(json_file)
                        src = os.path.join(molecules_folder,module_name, file)
                        defer = True
                        # Check if the file details already exist in the JSON data
                        if not any(entry['src'] == src and entry['defer'] == defer for entry in data['jsfiles']):
                            data['jsfiles'].append({
                                'src': src,
                                'defer': defer
                            })

                        json_file.seek(0)
                        json.dump(data, json_file, indent=4)
                        json_file.truncate()
