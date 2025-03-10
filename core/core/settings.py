"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
import sys
from pathlib import Path
from decouple import config
from celery import Celery

print(f"--- SYS01 settings.py START ---------------------------------------------------")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-#))__w==@v5a8d&8y0ylm#^t0nx7#i(09$$yq-cp$$@gbl*ml*'
SECRET_KEY = config('DJANGO_SECRET_KEY_SYS01')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = config('DEBUG', default=False, cast=bool)
DOCKER_ENV = config('DOCKER_ENV', default=False, cast=bool)

print(f'DEBUG {DEBUG}')
print(f'DOCKER_ENV {DOCKER_ENV}')

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'core',
    'crispy_forms',
    # 'crispy_bootstrap4',
    'crispy_bootstrap5',
    'management_commands',

    'commons',

    'pages',
    'users',
    'employees',
    'vendors',
    'customers',


    'products',

    'inventories',

    'approvers',
    'purchases',
    'sales',

    'analyses',

    'django_celery_results',
    'dbbackup',

    'rest_framework',

    # adding this will enable Auth Token in django admin
    'rest_framework.authtoken',
]
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if DEBUG:
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
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

WSGI_APPLICATION = 'core.wsgi.application'


# # use this style below if you want to set globally so that you don't need to set anything for each view/class for your api
# REST_FRAMEWORK = {
#     # make authentication token style
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.TokenAuthentication'
#     ],

#     # this makes all view class require permissions
#     # use the other one in the documentation for manual specific class permission
#     # 'DEFAULT_PERMISSION_CLASSES': [
#     # 	'rest_framework.permissions.IsAuthenticated'
#     # ]
# }


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

if DOCKER_ENV:
    DATABASE_HOST = config('DATABASE_PSYS_HOST', default='localhost')
else:
    DATABASE_HOST = 'localhost'
print(f'DATABASE_HOST {DATABASE_HOST}')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DATABASE_PSYS_NAME'),
        'USER': config('DATABASE_PSYS_USER'),
        'PASSWORD': config('DATABASE_PSYS_PASSWORD'),
        'HOST': DATABASE_HOST,
        'PORT': config('DATABASE_PSYS_PORT', default=5432),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # Default page size (client can override with `?page_size=20`)
    'PAGE_SIZE': 10,
}


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Manila'

USE_I18N = True

USE_TZ = True

# Celery settings
if DOCKER_ENV:
    CELERY_BROKER_URL = config(
        'CELERY_BROKER_URL', default='amqp://guest:guest@rabbitmq:5672//')
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
else:
    CELERY_BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = 'django-db'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
# do this if you use from django.contrib.auth import views as auth_views to manage your login
# so that django will not redirect to profile "default" after logging in
LOGIN_REDIRECT_URL = 'profile'
LOGOUT_REDIRECT_URL = 'login'
# users get redirected here if trying to access page that needs authentication
LOGIN_URL = 'login'


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = [
    '127.0.0.1',
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    'ENABLE_STACKTRACES': True,
    'INTERCEPT_REDIRECTS': False,
}

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': 'backup/'}
DBBACKUP_COMPRESS = False

# default is 1k. Increased to 3k to cater viewing tables with 365 days columns for datatables
DATA_UPLOAD_MAX_NUMBER_FIELDS = 3000

print(f"--- SYS01 settings.py END ---------------------------------------------------")
