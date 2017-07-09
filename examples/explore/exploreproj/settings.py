"""
Django settings for GTFS Explorer

First generated using Django 1.6.1
Quick-start development settings - unsuitable for production
"""

from decouple import config, Csv
import dj_database_url
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
_default_secret_key = 'l$hc*-biy7*#7cic5q5r^mtf-2&l34pq4k7znn%)si+$h(i%e&'
SECRET_KEY = config('SECRET_KEY', default=_default_secret_key, cast=str)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'exploreapp',
    'multigtfs',
]

LOCAL_INSTALLED_APPS = list(config('LOCAL_INSTALLED_APPS',
                                   default='', cast=Csv()))
INSTALLED_APPS.extend(LOCAL_INSTALLED_APPS)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'exploreproj.urls'

WSGI_APPLICATION = 'exploreproj.wsgi.application'

# Database
_default_db = 'spatialite:///%s' % os.path.join(BASE_DIR, 'db.sqlite3')
DATABASES = {'default': config('DATABASE_URL',
                               default=_default_db,
                               cast=dj_database_url.parse)}

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Test runner
_env_test_runner = config('TEST_RUNNER', default='', cast=str)
if _env_test_runner:
    TEST_RUNNER = _env_test_runner
