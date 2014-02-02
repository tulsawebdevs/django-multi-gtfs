multigtfs: The General Transit Feed Specification (GTFS) as a Django app
========================================================================

*multigtfs* is an `Apache 2.0`_-licensed Django app that supports importing
and exporting of GTFS feeds.  All features of the `June 20, 2012 reference`_
are supported.  It allows multiple feeds to be stored in the database at once.

It requires a spatial databases compatible with GeoDjango_.  PostgreSQL_ 9.x
and PostGIS_ 2.x are recommended for development and production, since these
support all the GeoDjango features.  There are issues with GeoDjango in
Django 1.4 (see `#20036`_), so Django 1.5 or above is recommended.

Usage
-----

Installation
++++++++++++
1. ``pip install multigtfs``
2. In your settings, add ``multigtfs`` to your ``INSTALLED APPS`` and ensure
   you have a spatial database configured.
3. ``./manage.py syncdb`` to install the tables, or ``./manage.py migrate`` if
   you are using South_

Management Commands
+++++++++++++++++++
There are two management commands to get GTFS feeds in and out of the database:

::

    ./manage.py importgtfs [--name name_of_feed] path/to/gtfsfeed.zip
    ./manage.py exportgtfs [--name basename_of_file] <feed_id>

In Code
+++++++
*multigtfs* is composed of Djangp models that implement GTFS, plus helper
methods for importing and exporting to the GTFS format.  Where GTFS relates
objects through IDs (such as Stop IDs for stops, *multigtfs* uses
ForeignKeys.

*multigtfs* includes a Feed object, which is not part of GTFS.  This is used
to include several feeds in the same file without collisions.  These can be
feeds from different agencies, or different versions of a feed from the same
agency.  The object has a helper method, ``in_feed``, that is sometimes useful
in filtering objects by feed.  At other times, it is easier to start at the
feed and follow relations.

There isn't separate documentation yet.  Load the app in your Django project,
play with the admin, and read the source code to learn more.

Project History
---------------
*multigtfs* was first developed for the `Tulsa Web Devs`_' project to get
Tulsa's buses into `Google Maps`_.  `tulsa-transit-google`_ is the the
Tulsa-specific portion, and *multigtfs* contains the parts useful for any
GTFS effort.  `Tulsa's bus schedule appeared on
Google Maps in July 2013`_, after a two-year effort.  The Tulsa Web Devs
founded `Code for Tulsa`_ to collaborate on future civic tech projects.

The conversion to _GeoDjango in February 2014 was generously sponsored by
MRCagney_.

Future
------
Upcoming features include:
- A sample project
- Validating the feed against Google's requirements
- More documentation
- More flexible GTFS imports and exports (longer values, extra columns)

See the `issues list`_ for more details.

.. _`Apache 2.0`: http://choosealicense.com/licenses/apache/
.. _`June 20, 2012 reference`: https://developers.google.com/transit/gtfs/reference
.. _GeoDjango: https://docs.djangoproject.com/en/dev/ref/contrib/gis/
.. _PostgreSQL: http://www.postgresql.org
.. _PostGIS: http://postgis.refractions.net
.. _South: http://south.readthedocs.org/en/latest/
.. _`Tulsa Web Devs`: http://tulsawebdevs.org
.. _`tulsa-transit-google`: https://github.com/tulsawebdevs/tulsa-transit-google
.. _`Google Maps`: https://www.google.com/intl/en/landing/transit/
.. _`Tulsa's bus schedule appeared on
Google Maps in July 2013`: http://tulsawebdevs.org/tulsa-transit-schedules-integrated-into-google-maps/
.. _`Code for Tulsa`: http://codefortulsa.org
.. _MRCagney: http://mrcagney.co.nz
.. _`issues_list`: https://github.com/tulsawebdevs/django-multi-gtfs/issues?state=open
.. _`#20036`: https://code.djangoproject.com/ticket/20036
