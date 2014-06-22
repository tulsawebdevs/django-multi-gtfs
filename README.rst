multigtfs: GTFS as a Django app
===============================

.. image:: https://travis-ci.org/tulsawebdevs/django-multi-gtfs.svg?branch=master
    :target: https://travis-ci.org/tulsawebdevs/django-multi-gtfs

**multigtfs** is an `Apache 2.0`_-licensed Django app that supports importing
and exporting of GTFS feeds.  All features of the `June 20, 2012 reference`_
are supported, including `all changes`_ up to February 17, 2014.
It allows multiple feeds to be stored in the database at once.

It requires a spatial databases compatible with GeoDjango_.  PostgreSQL_ 9.x
and PostGIS_ 2.x are recommended for development and production, since these
support all the GeoDjango features.  There are issues with GeoDjango in
Django 1.4 (see issue `20036`_), so Django 1.5 or above is recommended.

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

A third command will update cached geometries, used for making geo-queries at
the shape, trip, or route level:

::

    ./manage.py refreshgeometries --all   # Refresh all geometries
    ./manage.py refreshgeometries 1 2 3   # Refresh just feeds 1, 2, and 3

*Note*: cached geometries are normally updated whenever the related shape
points or stops are updated.  This command is useful for refreshing geometries
after manual changes or after a bug fix (like the v0.3.3 update).

In Code
+++++++
multigtfs is composed of Django models that implement GTFS, plus helper
methods for importing and exporting to the GTFS format.  Where GTFS relates
objects through IDs (such as Stop IDs for stops), multigtfs uses
ForeignKeys.

multigtfs includes a Feed object, which is not part of GTFS.  This is used
to include several feeds in the same file without collisions.  These can be
feeds from different agencies, or different versions of a feed from the same
agency.  The object has a helper method, ``in_feed``, that is sometimes useful
in filtering objects by feed.  At other times, it is easier to start at the
feed and follow relations.

There isn't separate documentation yet.  Load the app in your Django project,
play with the admin, and read the source code to learn more.

Sample Project
++++++++++++++
The `examples/explore` sample project demonstrates a simple read-only website
for viewing one or more GTFS feeds.  It include OpenLayers_ maps for viewing
the routes, trips, and shapes.  You an use it as is, or as a starting place
for your own projects.  See the project README for more information.

Project History
---------------
multigtfs was first developed for the `Tulsa Web Devs`_' project to get
Tulsa's buses into `Google Maps`_.  `tulsa-transit-google`_ is the
Tulsa-specific portion, and multigtfs contains the parts useful for any
GTFS effort.  `Tulsa's bus schedule appeared on
Google Maps in July 2013`_, after a two-year effort.  The Tulsa Web Devs
founded `Code for Tulsa`_ to collaborate on future civic tech projects.

Several features, including GeoDjango_ support and much faster feed imports,
were generously sponsored by MRCagney_.

Future
------
Upcoming features include:

- Validating the feed against Google's requirements
- More documentation

See the `issues list`_ for more details.

.. _`Apache 2.0`: http://choosealicense.com/licenses/apache/
.. _`June 20, 2012 reference`: https://developers.google.com/transit/gtfs/reference
.. _`all changes`: https://developers.google.com/transit/gtfs/changes#RevisionHistory
.. _GeoDjango: https://docs.djangoproject.com/en/dev/ref/contrib/gis/
.. _PostgreSQL: http://www.postgresql.org
.. _PostGIS: http://postgis.refractions.net
.. _South: http://south.readthedocs.org/en/latest/
.. _`Tulsa Web Devs`: http://tulsawebdevs.org
.. _`tulsa-transit-google`: https://github.com/tulsawebdevs/tulsa-transit-google
.. _`Google Maps`: https://www.google.com/intl/en/landing/transit/
.. _`Tulsa's bus schedule appeared on Google Maps in July 2013`: http://tulsawebdevs.org/tulsa-transit-schedules-integrated-into-google-maps/
.. _`Code for Tulsa`: http://codefortulsa.org
.. _MRCagney: http://mrcagney.co.nz
.. _`issues list`: https://github.com/tulsawebdevs/django-multi-gtfs/issues?state=open
.. _20036: https://code.djangoproject.com/ticket/20036
.. _OpenLayers: http://openlayers.org

