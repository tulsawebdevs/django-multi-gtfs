============
Installation
============

At the command line::

    $ easy_install multigtfs

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv multigtfs
    $ pip install multigtfs

In your settings, add ``multigtfs`` to your ``INSTALLED APPS`` and ensure
you have a spatial database configured.

Use ``./manage.py syncdb`` to install the tables, or ``./manage.py migrate``
if you are using South_

.. _South: http://south.readthedocs.org/en/latest/
