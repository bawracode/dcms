"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import sys
import os
import environ
from pathlib import Path
from nucleus.management.compilation import Compilation
from django.utils.translation import gettext_lazy as _

sys.path.append(os.path.join(Path(__file__).resolve().parent , 'nucleus'))


env = environ.Env(
  # set casting, default value
  DEBUG=(bool, False)
)
compilation = Compilation()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# reading .env file
environ.Env.read_env(env_file=os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = []


# Application definition
installed_apps = [
    # "adminlte3",
    # "adminlte3_theme",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'eav',
    'django_toggle_switch_widget',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'molecules',
    'nucleus',
    'django_cron',
]
CRON_CLASSES = [
    'molecules.api.cron.ClearAPILogsCronJob',
]


# Read the dynamic apps list from the file
dynamicappfile = os.path.join(compilation.compiled_dir, compilation.apps_file)
dynamic_apps = []
if os.path.exists(dynamicappfile):
    with open(dynamicappfile, 'r') as file:
        dynamic_apps = [app.strip() for app in file.readlines()]


# Add the dynamic apps to INSTALLED_APPS if not already present
INSTALLED_APPS = installed_apps + [app for app in dynamic_apps if app not in installed_apps]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'nucleus.middelware.middleware.RequestMiddleware',
    'molecules.api.middlewares.APILogMiddleware',
    'nucleus.middelware.middleware.AdminLanguageMiddleware',
    
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'api_calls.log',  # Specify the log file name and location
        },
    },
    'loggers': {
        'api_calls': {
            'handlers': ['file', 'console'],  # Use both file and console handlers
            'level': 'INFO',
        },
    },
}

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env("DB_NAME"),  
        'USER': env("DB_USER"),  
        'PASSWORD': env("DB_PASSWORD"),  
        'HOST': env("DB_HOST"),  
        'PORT': env("DB_PORT"),  
        'OPTIONS': {  
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"  
        } 
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#for language


LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
    ('es', _('Spanish')),
    ('de', _('German')),
    
)

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]
