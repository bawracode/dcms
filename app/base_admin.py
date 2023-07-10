from django.contrib import admin
from django.utils.safestring import mark_safe

from nucleus.controller.main_controller import ColumnController
from nucleus.users.models import UserPrefrenceModel
import json
from django.contrib.admin.views.main import ChangeList

class CustomChangeList(ChangeList):
    def __init__(self, *args, **kwargs):
        request = kwargs['request']
        self.list_per_page = int(request.GET.get('list_per_page', self.list_per_page))
        super().__init__(*args, **kwargs)

class BaseModelAdmin(admin.ModelAdmin):
    list_display=[]
    list_filter=[]
    list_per_page=10
    


    def action(self, obj):
        return mark_safe(f'''
                         <a href="{obj.id}/change/"><img src="/static/admin/img/icon-changelink.svg" alt="True"></a> \t\t
                         <a href="{obj.id}/delete/"><img src="/static/admin/img/icon-deletelink.svg" alt="True"></a>''')
    action.short_description = 'Action'

    
    def get_column_names_and_user_prefrences(self,user):
        
        model = self.model
        path_model=str(self).replace('.','_')
        columns_mapper=ColumnController()
        prefrence_found=UserPrefrenceModel.objects.filter(user=user,model_path=path_model).first()
        if prefrence_found:
           output=prefrence_found.json_data
           output=sorted(output, key=lambda x: x["sort_order"])
        
           columns_mapper.set_dict(output)
           
           self.list_display=columns_mapper.get_list_display()
           
        
        else:
            #default list display list for admin
            column_list = [field.name for field in model._meta.get_fields()]
            self.list_display=['action']+column_list
            #sortable views list for admin
            template = {"visible": True, "sort_order": None, "column_name": None}
            
            output = [template.copy() for _ in range(len(column_list))]
            for i, column_name in enumerate(column_list):
                output[i]["column_name"] = column_name
        
        columns_mapper.set_model(model)
        self.list_filter=columns_mapper.get_list_filter()
        return output,path_model
    def changelist_view(self, request, extra_context=None):
        if request.GET.get('list_per_page'):
            self.list_per_page = int(request.GET['list_per_page'])
        
        extra_context = extra_context or {}
        username=request.user.id
        column_names,path_model = self.get_column_names_and_user_prefrences(username)

        
        #sortable list columns
        extra_context['column_names'] = column_names
        serialized_data = json.dumps(column_names)
        extra_context['serialized_data'] = serialized_data
        extra_context['path_model']=path_model
        
        return super().changelist_view(request, extra_context)

    
    