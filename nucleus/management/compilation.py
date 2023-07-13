import os
from pathlib import Path

class Compilation:
    def __init__(self):
        self.compiled_dir = os.path.join( Path(__file__).resolve().parent.parent ,'compiled')
        self.apps_file = 'compiled_apps.txt'

class Compilation_config:
    def __init__(self):
        self.compiled_dir = os.path.join( Path(__file__).resolve().parent.parent ,'compiled')
        self.config_file = 'compiled_config.json'