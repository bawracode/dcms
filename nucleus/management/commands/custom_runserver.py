import os
from django.core.management.base import BaseCommand
from django.core.management.commands.runserver import Command as RunserverCommand
import os
import json
from pathlib import Path


class Command(RunserverCommand):
    help = "Starts the custom runserver."
    

    def handle(self, args, *options):
        base_directory = Path(__file__).resolve().parent.parent.parent.parent
        modul_list = []
        for filename in os.listdir(os.path.join(base_directory,'molecules')):
            modul_list.append(filename,'active')

        dictionary = {}
        for i in range(0, len(modul_list), 2):
            key = modul_list[i]
            value = modul_list[i + 1]
            dictionary[key] = value

        with open(os.path.join(base_directory,'mainConfig.json'), 'w') as config_file:
             json.dump(dictionary, config_file, indent=4)


        super().handle(*args, **options)

