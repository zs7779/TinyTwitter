"""
Django settings for tinytwitter project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import json
import logging.config
from django.urls import reverse


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', "foobar")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', "True") == "True"

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# Application definition

INSTALLED_APPS = [
    'network',
    'frontend',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tinytwitter.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'tinytwitter.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.{}'.format(
             os.getenv('DATABASE_ENGINE', 'sqlite3')
         ),
         'NAME': os.getenv('DATABASE_NAME', os.path.join(BASE_DIR, 'db.tinytwitter')),
         'USER': os.getenv('DATABASE_USERNAME', 'myprojectuser'),
         'PASSWORD': os.getenv('DATABASE_PASSWORD', 'password'),
         'HOST': os.getenv('DATABASE_HOST', 'db'),
         'PORT': os.getenv('DATABASE_PORT', 5432),
         'OPTIONS': json.loads(
             os.getenv('DATABASE_OPTIONS', '{}')
         ),
     }
}

AUTH_USER_MODEL = "network.User"

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Logging Configuration
if not DEBUG:
    # Clear prev config
    LOGGING_CONFIG = None

    # Get loglevel from env
    LOGLEVEL = os.getenv('DJANGO_LOGLEVEL', 'info').upper()

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console': {
                'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'console',
            },
        },
        'loggers': {
            '': {
                'level': LOGLEVEL,
                'handlers': ['console',],
            },
        },
    })


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
# STATIC_ROOT = '../../homepage/dist/tinytwitter/'
STATIC_URL = '/static/'
# STATIC_URL = '/static/' if DEBUG else 'https://zhaosean.com/dist/tinytwitter/'
LOGIN_URL = '/login/'