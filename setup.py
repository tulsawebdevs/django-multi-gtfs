#!/usr/bin/env python

from setuptools import setup, find_packages

# Get the version from __init__.py
__version__ = None
execfile('multigtfs/__init__.py')  # Should redefine __version__

setup(
    name='multigtfs',
    version=__version__,
    description='General Transit Feed Specification (GTFS) as Django app',
    author='John Whitlock',
    author_email='John-Whitlock@ieee.org',
    license='Apache License 2.0',
    url='https://github.com/tulsawebdevs/django-multi-gtfs',
    packages=find_packages(),
    install_requires=['Django>=1.3'],
    keywords='django gtfs',
)
