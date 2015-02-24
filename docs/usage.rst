========
Usage
========

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

See the next section, `Implementation of GTFS`_, for details on how the GTFS
specification is implemented in Django models.  Load the app in your Django
project, play with the admin, and read the source code to learn more.

Sample Project
++++++++++++++
The ``examples/explore`` sample project demonstrates a simple read-only website
for viewing one or more GTFS feeds.  It include OpenLayers_ maps for viewing
the routes, trips, and shapes.  You can use it as is, or as a starting place
for your own projects.  See the project README (``examples/explore/README.md``)
for more information.

.. _OpenLayers: http://openlayers.org
.. _`Implementation of GTFS`: gtfs.html
