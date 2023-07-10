import os
from pathlib import Path
from app import custom_filter
from django.contrib import admin
class Compilation:
    def __init__(self,file_name):
        self.compiled_dir = os.path.join( Path(__file__).resolve().parent.parent ,'compiled')
        self.apps_file = file_name


class ColumnController:
    def set_dict(self,column_dict):
        self.column_dict = column_dict
    def set_model(self,model):
        self.model=model
    def get_list_display(self):
        list_columns=('action',)
        list_columns+=tuple(item["column_name"] for item in self.column_dict if item.get("visible", False))
        return list_columns
    def get_list_filter(self):

        model_fields = self.model._meta.get_fields()
        filter=()
        for field in model_fields:
            field_name = field.name
            field_type = field.get_internal_type()
            choices = getattr(field, 'choices', None)
            if choices:
                filter += ((field_name, custom_filter.TextDropDownFilter),)
                print(f"Field Name: {field_name}, Field Type: {field_type}, Choices: {choices}")
            else:
                if field_type in ["CharField","SlugField","TextField"]:
                    filter += ((field_name, custom_filter.TextInputFilter),)
                if field_type=='DateTimeField':
                    filter+=((field_name,admin.DateFieldListFilter),)
                    
                print(f"Field Name: {field_name}, Field Type: {field_type}")


        
        
        return filter
    
