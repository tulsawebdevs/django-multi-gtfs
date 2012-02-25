#!/usr/bin/env python

from distutils.core import setup

setup(name='django-gtfs',
      version='0.1.1',
      description='General Transit Feed Specification (GTFS) as Django app',
      author='John Whitlock',
      author_email='John-Whitlock@ieee.org',
      license='Apache License 2.0',
      url='https://github.com/tulsawebdevs/django-gtfs',
      packages=['django_gtfs', 'django_gtfs.models'],
      package_dir={'' : 'src'},
      keywords='django gtfs',
     )
