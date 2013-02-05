#!/usr/bin/env python
# Copyright 2012 John Whitlock
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

import sys

from django.conf import settings


def main():
    # Dynamically configure the Django settings with the minimum necessary to
    # get Django running tests
    INSTALLED_APPS = ['multigtfs']
    TEST_RUNNER = 'django.test.simple.DjangoTestSuiteRunner'

    # If django-nose is installed, use it
    # You can do things like ./run_tests.py --with-coverage
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

    settings.configure(
        INSTALLED_APPS=INSTALLED_APPS,
        # Django replaces this, but it still wants it. *shrugs*
        DATABASE_ENGINE='django.db.backends.sqlite3',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        DEBUG=True, TEMPLATE_DEBUG=True, TEST_RUNNER=TEST_RUNNER
    )

    from django.core import management
    failures = management.call_command('test')  # Will pull sysv args itself
    sys.exit(failures)


if __name__ == '__main__':
    main()
