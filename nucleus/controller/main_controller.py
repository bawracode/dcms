import os
from pathlib import Path

class Compilation:
    def __init__(self,file_name):
        self.compiled_dir = os.path.join( Path(__file__).resolve().parent.parent ,'compiled')
        self.apps_file = file_name

        