import os
from pathlib import Path

class Compilation:
    def __init__(self,file_name):
        self.compiled_dir = os.path.join( Path(__file__).resolve().parent.parent ,'compiled')
        self.apps_file = file_name


class ColumnController:
    def __init__(self,column_dict):
        self.column_dict = column_dict

    def get_list_display(self):
        list_columns=('action',)
        list_columns+=tuple(item["column_name"] for item in self.column_dict if item.get("visible", False))
        return list_columns
    def get_list_filter(self):
        desired_filters = tuple((item["column_name"], item["filter"]) for item in self.column_dict if item["filter"] is not None)
        return desired_filters
    
