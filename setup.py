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
import sys
# Get the version from __init__.py
from multigtfs import __version__


class my_test(test):
    def run(self):
        import run_tests
        run_tests.main()


def get_long_description():
    import codecs
    with codecs.open('README.rst', 'r', 'utf-8') as f:
        readme = f.read()

    body_tag = ".. Omit badges from docs"
    readme_body_start = readme.index(body_tag)
    assert readme_body_start
    readme_body = readme[readme_body_start + len(body_tag):]

    with codecs.open('CHANGELOG.rst', 'r', 'utf-8') as f:
        changelog = f.read()
    old_tag = ".. Omit older changes from package"
    changelog_body_end = changelog.index(old_tag)
    assert changelog_body_end
    changelog_body = changelog[:changelog_body_end]

    long_description = """
%(readme_body)s

%(changelog_body)s

Older changes can be found in the `full documention`_.

.. _`full documention`: \
http://multigtfs.readthedocs.io/en/latest/changelog.html
""" % locals()
    return long_description


# Handle Py2/Py3 issue
if sys.version_info > (3, 0):
    # In Py3, package data is dict w/ text key
    package_data = {'multigtfs': ['tests/fixtures/*.zip']}
else:
    # In Py2, package data is dict w/ binary string
    package_data = {b'multigtfs': ['tests/fixtures/*.zip']}


setup(
    name='multigtfs',
    version=__version__,
    description='General Transit Feed Specification (GTFS) as a Django app',
    long_description=get_long_description(),
    author='John Whitlock',
    author_email='John-Whitlock@ieee.org',
    license='Apache License 2.0',
    url='https://github.com/tulsawebdevs/django-multi-gtfs',
    packages=find_packages(),
    install_requires=['Django>=1.8', 'jsonfield>=0.9.20'],
    keywords=['django', 'gtfs'],
    test_suite="run_tests",  # Ignored, but makes pyroma happy
    cmdclass={'test': my_test},
    zip_safe=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
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
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    include_package_data=True,
    package_data=package_data
)
