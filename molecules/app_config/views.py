import json
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
import importlib

import json

def update_value():
        with open('molecules/app_config/app_config.json') as json_file:
            json_data = json.load(json_file)

# update default value
def update_default_value(data, key, new_value):
    if isinstance(data, dict):
        if "default" in data and data.get("key") == key:
            data["default"] = new_value
        for k, v in data.items():
            update_default_value(v, key, new_value)
    elif isinstance(data, list):
        for item in data:
            update_default_value(item, key, new_value)

#load json file
with open('molecules/app_config/app_config.json') as json_file:
    json_data = json.load(json_file)

# from molecules.test1.source.status import status

# find source
def find_source(json_data, search_key):
    for section in json_data:
        for sub_section in section["sub"]:
            for field in sub_section["fields"]:
                if field["key"] == search_key:
                    return field["source"]
    return None



# Create your views here.
def index(request):
    return HttpResponse("app_config")

# return section
def return_sub_section(request):
    
    
    if request.method == 'POST':
        data = json.loads(request.body)
        section_name = data['section_name']

        for i in json_data:
            if i.get('section') == section_name:
                sub_section = i.get('sub')
                break

        response_data = {
            'sub_section': sub_section,
            'status': 'success'
        }

        return JsonResponse(response_data)

    response_data = {
        'message': 'Invalid request',
        'status': 'error'
    }

    return JsonResponse(response_data, status=400)


# return field
def return_option(request):

    if request.method == "POST":
        data = json.loads(request.body)
        key = data['key']
        
        result = find_source(json_data,key)

        temp_module = result.split('_')
        module = ".".join(temp_module)
        module = importlib.import_module(f"{module}")
        class_name = temp_module[-1]

        class_obj = getattr(module, class_name)

        instance = class_obj()

        response_data = {
            'options': instance.return_options(),
            'status': 'success'
        }
        return JsonResponse(response_data)

# save value
def save_value(request):
    if request.method == "POST":
        data = json.loads(request.body)
        form_field = data['form_field']
        print(form_field)
        for i in form_field:
            key = i
            value = form_field[i]

            update_default_value(json_data, key, value)

        with open('molecules/app_config/app_config.json', 'w') as outfile:
            json.dump(json_data, outfile, indent=4)

        update_value()

        response_data = {
            'status': 'success'
        }

        return JsonResponse(response_data)