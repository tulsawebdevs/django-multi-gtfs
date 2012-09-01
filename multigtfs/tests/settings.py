# Fake settings for test
INSTALLED_APPS = [
    'multigtfs'
]

# If django-nose is installed, use it
try:
    from pkg_resources import WorkingSet, DistributionNotFound
    working_set = WorkingSet()
    working_set.require('django_nose')
except ImportError:
    print 'setuptools not installed.  Weird.'
except DistributionNotFound:
    print "django-nose not installed.  You'd like it."
else:
    INSTALLED_APPS.append('django_nose')
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'multigtfs.db',
    },
}
