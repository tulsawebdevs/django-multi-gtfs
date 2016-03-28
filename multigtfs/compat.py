"""Compatibility utilities.

Handle compatibility between Python versions, Django versions, etc.
"""
from distutils.version import StrictVersion

from django import get_version
from django.db.models import Field

DJ_VERSION = StrictVersion(get_version())


#
# Get the base class for custom model fields
#

if DJ_VERSION >= StrictVersion('1.8'):
    # Django 1.8 and later - Custom Fields just override Field
    FieldBase = Field
else:
    # Django 1.7 and lower require SubfieldBase
    from django.db.models import SubfieldBase
    from django.utils.six import with_metaclass
    FieldBase = with_metaclass(SubfieldBase, Field)
