"""Compatibility utilities.

Handle compatibility between Python versions, Django versions, etc.
"""
from codecs import BOM_UTF8
from distutils.version import LooseVersion

from django import get_version
from django.utils.six import PY3, binary_type

DJ_VERSION = LooseVersion(get_version())


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


def bom_prefix_csv(text):
    """
    Prefix CSV text with a Byte-order Marker (BOM).

    The return value needs to be encoded differently so the CSV reader will
    handle the BOM correctly:
    - Python 2 returns a UTF-8 encoded bytestring
    - Python 3 returns unicode text
    """
    if PY3:
        return BOM_UTF8.decode('utf-8') + text
    else:
        return BOM_UTF8 + text.encode('utf-8')


def force_utf8(text):
    """Encode as UTF-8 bytestring if it isn't already."""
    if isinstance(text, binary_type):
        return text
    else:
        return text.encode('utf-8')


def opener_from_zipfile(zipfile):
    """
    Returns a function that will open a file in a zipfile by name.

    For Python3 compatibility, the raw file will be converted to text.
    """

    def opener(filename):
        inner_file = zipfile.open(filename)
        if PY3:
            from io import TextIOWrapper
            return TextIOWrapper(inner_file)
        else:
            return inner_file

    return opener