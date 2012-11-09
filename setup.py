#!/usr/bin/env python
#
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
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    long_description="""\
General Transit Feed Specification (GTFS) as a Django app
---------------------------------------------------------

multigtfs supports importing and exporting of GTFS feeds.  All features of the
June 20, 2012 reference are supported. See
https://developers.google.com/transit/gtfs/reference for more information.

multigtfs is designed to allow multiple feeds to be stored in the database
at once.

"""
)
