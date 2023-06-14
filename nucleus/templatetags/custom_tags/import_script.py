from django import template
import environ
import os
from django.conf import settings
import json
from django.urls import resolve

env = environ.Env(
  DEBUG=(bool, False)
)

environ.Env.read_env(env_file=os.path.join(settings.BASE_DIR, ".env"))

app_folder = env("APP_FOLDER")

register = template.Library()

config_app = 0

@register.simple_tag(takes_context=True)
def apps_script(context):
    request = context['request']
    app = resolve(request.path_info).app_name
  
    if os.path.isdir(os.path.join(app_folder, app)):
            with open(settings.BASE_DIR.joinpath(app_folder).joinpath(app).joinpath("config.json")) as f:
                temp_file = json.loads(f.read())
                config_app = temp_file
    js_files = config_app.get("js")

    scripts = ""

    for i in js_files:
         src = i.get("src")
         defer = i.get("defer")

         defer_str = "defer" if defer else ""

         temp_script_str =f"<script src='"+src+"'"+defer_str+"></script>"

         scripts += temp_script_str

    return scripts
         

    
