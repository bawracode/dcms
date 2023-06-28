from django.contrib import admin
from .models import Blocks
from django import forms
from app import custom_filter

class BlocksForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 30, 'cols': 100}),  # Adjust rows and cols values as per your preference
    )

    class Meta:
        model = Blocks
        fields = '__all__'

# Register your models here.
@admin.register(Blocks)
class BlockAdmin(admin.ModelAdmin):
    form = BlocksForm
    list_display = ("id",'slug', 'status',"block_status",'created_at', 'updated_at',"formatted_full_url")
    list_filter = (
        ('slug', custom_filter.TextInputFilter),
        ('status', custom_filter.TextDropDownFilter),
        ('block_status', custom_filter.TextDropDownFilter),
        # Add more filters for other fields
    )
    # list_filter=("slug",)
    