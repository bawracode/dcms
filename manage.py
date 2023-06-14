#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import json


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)




def update_json_file():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    app_folder = os.getenv("APP_FOLDER")
    config_app = []

    for app in os.listdir(app_folder):
        app_path = os.path.join(app_folder, app)
        if os.path.isdir(app_path):
            print(app)
            config_file_path = os.path.join(base_dir, app_path, "config.json")
            with open(config_file_path) as f:
                temp_file = json.loads(f.read())
                config_app.append(temp_file)

    status_list = {}

    for i in config_app:
        status_list[i.get("app_name")] = i.get("status")

    main_config_path = os.path.join(base_dir, "main_config.json")

    with open(main_config_path, 'w') as status_file:
        status_file.write(json.dumps(status_list))

    print("Updated main_config.json")


if __name__ == "__main__":
    update_json_file()
    main()

