# Rename to local_settings.py, adjust settings below

# Add django_extensions for ./manage.py runserver_plus, shell_plus, etc.
LOCAL_INSTALLED_APPS = ['django_extensions']

# Use PostGIS for backend
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'explore',
        'USER': 'explore',
        'PASSWORD': 'explore',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
