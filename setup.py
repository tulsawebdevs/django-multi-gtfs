#!/usr/bin/env python

from distutils.core import setup

setup(
    name='multigtfs',
    version='0.1.3',
    description='General Transit Feed Specification (GTFS) as Django app',
    author='John Whitlock',
    author_email='John-Whitlock@ieee.org',
    license='Apache License 2.0',
    url='https://github.com/tulsawebdevs/django-multi-gtfs',
    packages=['multigtfs', 'multigtfs.models'],
    keywords='django gtfs',
)
