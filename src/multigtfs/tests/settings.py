# Fake settings for test
INSTALLED_APPS = [
    'multigtfs'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'multigtfs.db',
    },
}
