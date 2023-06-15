from django.contrib import admin
from molecules.cms.pages.models import CustomPage
from django.conf import settings
import os
from django import forms

def create_templates():
    base_directory = settings.BASE_DIR

    if not os.path.exists(os.path.join(base_directory, 'templates')):
        os.makedirs(os.path.join(base_directory, 'templates'))
    if not os.path.exists(os.path.join(base_directory, 'templates', 'pages')):
        os.makedirs(os.path.join(base_directory, 'templates', 'pages'))
    if not os.path.exists(os.path.join(base_directory, 'templates', 'pages', 'admin')):
        os.makedirs(os.path.join(base_directory, 'templates', 'pages', 'admin'))
    if not os.path.exists(os.path.join(base_directory, 'templates', 'pages', 'admin', 'custom_change_form.html')):
        with open(os.path.join(base_directory, 'templates', 'pages', 'admin', 'custom_change_form.html'), 'w') as f:
            f.write("""
            {% extends "admin/change_form.html" %}
{% block breadcrumbs %}

<div class="row mb-2">
    <div class="col-sm-4">
        <h2>{{title}}</h2>
    </div>

    {% endblock %}
{% block after_related_objects %}

{{ block.super }}
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
{% endblock %}

""")
create_templates()
# Register your models here.
class PagesForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 30, 'cols': 100}),  # Adjust rows and cols values as per your preference
    )

    class Meta:
        model = CustomPage
        fields = '__all__'

class CustomePageAdmin(admin.ModelAdmin):
    form = PagesForm
    list_display = ('title', 'slug', 'status', 'created_at', 'updated_at','formatted_full_url')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    change_form_template = "pages/admin/custom_change_form.html"
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

admin.site.register(CustomPage, CustomePageAdmin)
