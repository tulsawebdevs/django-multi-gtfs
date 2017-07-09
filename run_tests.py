#!/usr/bin/env python
# Copyright 2012-2014 John Whitlock
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Thanks to django-extensions for the starting code

from __future__ import print_function
import sys

import django
from django.conf import settings

django_version, django_point = django.VERSION[:2]


def base_config():
    '''Create a minimal Django configuration'''
    return {
        'INSTALLED_APPS': ['multigtfs'],
        'TEST_RUNNER': 'django.test.runner.DiscoverRunner',
        'DATABASE_ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'DATABASES': {
            'default': {
                'ENGINE': 'django.contrib.gis.db.backends.spatialite',
            }
        },
        'DEBUG': True,
        'TEMPLATE_DEBUG': True,
        'MIDDLEWARE_CLASSES': '',
    }


def test_config():
    '''Create a Django configuration for running tests'''

    config = base_config()

    # If django-nose is installed, use it
    # You can do things like ./run_tests.py --with-coverage
    try:
        from pkg_resources import WorkingSet, DistributionNotFound
        working_set = WorkingSet()
        working_set.require('django_nose')
    except ImportError:
        print('setuptools not installed.  Weird.')
    except DistributionNotFound:
        print("django-nose not installed.  You'd like it.")
    else:
        config['INSTALLED_APPS'].append('django_nose')
        config['TEST_RUNNER'] = 'django_nose.NoseTestSuiteRunner'

    # Optionally update configuration
    try:
        import t_overrides
    except ImportError:
        pass
    else:
        config = t_overrides.update(config)

    return config


def main(*paths):
    config = test_config()
    settings.configure(**config)
    django.setup()

    from django.core import management
    failures = management.call_command(
        'test',
        *paths
    )
    sys.exit(failures)


if __name__ == '__main__':
    # Extract non-options from command line
    # Options (-sx, --ipdb) will be parsed inside call_command
    paths = []
    for arg in sys.argv[1:]:
        if not arg.startswith('-'):
            paths.append(arg)

    main(*paths)
