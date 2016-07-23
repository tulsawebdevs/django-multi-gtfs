"""Compatibility utilities.

Handle compatibility between Python versions, Django versions, etc.
"""
from distutils.version import LooseVersion

from django import get_version
from django.db.models import Field

DJ_VERSION = LooseVersion(get_version())


#
# Get the base class for custom model fields
#

if DJ_VERSION >= LooseVersion('1.8'):
    # Django 1.8 and later - Custom Fields just override Field
    FieldBase = Field
else:
    # Django 1.7 and lower require SubfieldBase
    from django.db.models import SubfieldBase
    from django.utils.six import with_metaclass
    FieldBase = with_metaclass(SubfieldBase, Field)


#
# Get the 'blank' value for a field
#

def _get_blank_value_18(field):
    """Get the value for blank fields in Django 1.8 and earlier."""
    if field.null:
        return None
    else:
        return field.value_to_string(None)


def _get_blank_value_19(field):
    """Get the value for blank fields in Django 1.9 and later."""
    if field.null:
        return None
    else:
        return ''

if DJ_VERSION >= LooseVersion('1.9'):
    get_blank_value = _get_blank_value_19
else:
    get_blank_value = _get_blank_value_18
