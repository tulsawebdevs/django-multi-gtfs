#!/usr/bin/env python
#
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
from __future__ import unicode_literals

from setuptools import setup, find_packages
from setuptools.command.test import test
import os
# Get the version from __init__.py
from multigtfs import __version__


class my_test(test):
    def run(self):
        import run_tests
        run_tests.main()


def read(*paths):
    with open(os.path.join(*paths), 'r') as f:
        return f.read()


setup(
    name='multigtfs',
    version=__version__,
    description='General Transit Feed Specification (GTFS) as a Django app',
    author='John Whitlock',
    author_email='John-Whitlock@ieee.org',
    license='Apache License 2.0',
    url='https://github.com/tulsawebdevs/django-multi-gtfs',
    packages=find_packages(),
    install_requires=['Django>=1.5', 'jsonfield>=0.9.20'],
    keywords='django gtfs',
    test_suite="run_tests",  # Ignored, but makes pyroma happy
    cmdclass={'test': my_test},
    zip_safe=True,
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
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    long_description=(
        read('README.rst') + '\n\n' +
        read('CHANGELOG.rst') + '\n\n' +
        read('AUTHORS.rst'))
)
