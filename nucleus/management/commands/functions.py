import os
from django.conf import settings
import environ

env = environ.Env(
  # set casting, default value
  DEBUG=(bool, False)
)

environ.Env.read_env(env_file=os.path.join(settings.BASE_DIR, ".env"))

app_folder = env("APP_FOLDER")

#return app name
def all_apps():
    molecular_apps = [
    app_name
    for app_name in os.listdir(app_folder)
    if os.path.isdir(os.path.join(app_folder, app_name))
    ]

    return molecular_apps

#return app name from templates folder
def apps_templates():
    return [
    app_name
    for app_name in os.listdir("templates")
    if os.path.isdir(os.path.join("templates", app_name))
    ]

#{
#                     "src": "/static/js/{0}/x.js".format(app),
#                     "defer":0
#                 }