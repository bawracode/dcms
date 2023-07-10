from django.contrib import admin
from .models import Blocks
from django import forms

from app import base_admin


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
    prepopulated_fields = {'slug': ('title',)}
    
    
    