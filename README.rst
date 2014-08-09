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

.. _`Apache 2.0`: http://choosealicense.com/licenses/apache/
.. _`June 20, 2012 reference`: https://developers.google.com/transit/gtfs/reference
.. _`all changes`: https://developers.google.com/transit/gtfs/changes#RevisionHistory
.. _PostgreSQL: http://www.postgresql.org
.. _PostGIS: http://postgis.refractions.net
.. _20036: https://code.djangoproject.com/ticket/20036
.. _GeoDjango: https://docs.djangoproject.com/en/dev/ref/contrib/gis/
