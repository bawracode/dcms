from django.contrib import admin
from django.contrib.admin import FieldListFilter
from django.template.loader import get_template
from django.utils.html import format_html
from django.utils.text import capfirst
class TextDropDownFilter(FieldListFilter):
    template = 'admin/custom_text_dropdown.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.field_path = field_path
        self.model_admin = model_admin
        self.model = model_admin.model  # Get the model from the model_admin
        super().__init__(field, request, params, model, model_admin, field_path)

    def expected_parameters(self):
        return [self.field_path]

    def choices(self, changelist):
        queryset = changelist.queryset
        values = queryset.values_list(self.field_path, flat=True).distinct()
        choices = []
        selected_value = self.used_parameters.get(self.field_path)  # Get the currently selected value
        choices.append({
            'selected': not selected_value,  # Set "All" as selected if no value is selected
            'query_string': changelist.get_query_string(remove=[self.field_path]),
            'display': 'All',
        })

        # Get the model field for the specified field path
        model_field = self.model._meta.get_field(self.field_path)
        

        for value in set(values):
            
            display_value = dict(model_field.choices).get(value)
            
            choice = {
                'selected': str(value) == str(selected_value),
                'query_string': changelist.get_query_string({self.field_path: value}),
                'display': capfirst(display_value) if display_value else str(value),
            }
            
            choices.append(choice)

        # Add an additional choice for "All" option
        

        

        return choices

    def queryset(self, request, queryset):
        value = self.used_parameters.get(self.field_path)  # Get the currently selected value
        
        if value:
            kwargs = {
                self.field_path: value,
            }
            return queryset.filter(**kwargs)

        return queryset
    def get_template(self):
        return get_template(self.template)

    def value(self):
        return self.used_parameters.get(self.field_path)

class TextInputFilter(FieldListFilter):
    template = 'admin/custom_text_input_filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.field = field
        super().__init__(field, request, params, model, model_admin, field_path)

    def expected_parameters(self):
        return [self.field_path]

    def choices(self, changelist):
        print(self.value())
        yield {
            'selected': self.value(),
            'query_string': changelist.get_query_string({self.field: None}, []),
            'display': 'All',
        }

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            kwargs = {
                f'{self.field_path}__icontains': value,
            }
            return queryset.filter(**kwargs)

        return queryset

    def get_template(self):
        return get_template(self.template)

    def value(self):
        return self.used_parameters.get(self.field_path) or self.used_parameters.get(self.field_path + '__icontains')
