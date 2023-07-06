from django.contrib import admin
from .models import Blocks
from django import forms
from app import custom_filter
from nucleus.controller.main_controller import ColumnController
from app import base_admin

columns_in_use=[
    {"column_name":"id","visible":True,"sort_order":10,"filter":None},
    {"column_name":"title","visible":False,"sort_order":20,"filter":None},
    {"column_name":"content","visible":False,"sort_order":30,"filter":None},
    
    {"column_name":"slug","visible":True,"sort_order":20,"filter":custom_filter.TextInputFilter},
    {"column_name":"status","visible":True,"sort_order":30,"filter":custom_filter.TextDropDownFilter},
    {"column_name":"block_status","visible":True,"sort_order":40,"filter":custom_filter.TextDropDownFilter},
    {"column_name":"created_at","visible":True,"sort_order":50,"filter":None},
    {"column_name":"updated_at","visible":True,"sort_order":60,"filter":None},
    {"column_name":"formatted_full_url","visible":None,"sort_order":70,"filter":None},
]
class BlocksForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 30, 'cols': 100}),  # Adjust rows and cols values as per your preference
    )

    class Meta:
        model = Blocks
        fields = '__all__'



# Register your models here.
@admin.register(Blocks)
class BlockAdmin(base_admin.BaseModelAdmin):
    form = BlocksForm
       
    columns=ColumnController(columns_in_use)
    list_display = columns.get_list_display()
    
    list_filter = columns.get_list_filter()
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['columns']=columns_in_use
        return super().changelist_view(request, extra_context)
    prepopulated_fields = {'slug': ('title',)}
    # list_filter=("slug",)
    