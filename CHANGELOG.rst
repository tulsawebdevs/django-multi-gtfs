Changelog
=========

1.1.1 (2017-08-02)
------------------
* Strip whitespace after commas in CSV files with skipinitialspace_
  (`issue #64`_, `PR #65`_ and `#68`_).
* Discard empty lines in CSV files (`issue #66`_, `PR #67`_)

.. _skipinitialspace: https://docs.python.org/2/library/csv.html#csv.Dialect.skipinitialspace
.. _`issue #64`: https://github.com/tulsawebdevs/django-multi-gtfs/issues/64
.. _`PR #65`: https://github.com/tulsawebdevs/django-multi-gtfs/pull/65
.. _`#68`: https://github.com/tulsawebdevs/django-multi-gtfs/pull/68
.. _`issue #66`: https://github.com/tulsawebdevs/django-multi-gtfs/issues/66
.. _`PR #67`: https://github.com/tulsawebdevs/django-multi-gtfs/pull/67

1.1.0 (2017-07-09)
------------------
* Add support for Django 1.10 and 1.11
* Drop support for Django 1.7 and earlier, and for South migrations. If you
  are using these, upgrade to 1.0.0 first, migrate your codebase to Django 1.8
  and Django migrations, then update to 1.1.0.
* Move Python 2 / Python 3 and other compatibilty code to
  ``multigtfs/compat.py``.  Exclude this file from the ``make qa`` coverage
  report, unless the ``COVERAGE_COMPAT`` environment variable is set.  Because
  the cross-environment code is now in this file, many lines will be uncovered
  in a particular environment, while other files should be 100% covered. This
  file is tested in the supported environments in TravisCI, and a combined
  coverage report is generated in Coveralls, where ``compat.py`` should be 100%
  covered.
* Add a dockerized environment for the explore example app, and run it under
  Django 1.11.
* Whitespace-only values in import files are treated as empty values
  (`PR #56`_)

.. _`PR #56`: https://github.com/tulsawebdevs/django-multi-gtfs/pull/56

1.0.0 (2016-03-29)
------------------
* The project has been production-ready for a while. Updating the version
  number and the PyPI classifiers to reflect that.
* Add support for Django 1.7 through 1.9, and a compatibility layer to handle
  future versions.
* Add support for transitioning from South to Django migrations.

.. Omit older changes from package

0.4.3 (2015-02-24)
------------------
* Added documentation (issue #26)
* exportgtfs uses compression if available.  Reduces one exported feed from
  141MB to 21MB. (issue #27)
* Feeds that omit calendar.txt can be imported and exported.  GTFS allows this
  if all dates are specified in calendar_dates.txt instead.  This alternate
  format is used by the TriMet archive feeds from Portland, OR (issue #28).
* Django 1.7 is *not* supported by multigtfs.  Version is limited in setup.py
  to 1.5 and 1.6.

0.4.2 (2014-07-20)
------------------
* importgtfs handles feeds with whitespace strings (issue #36)
* Can update objects with JSON fields in admin (issue #37)
* importgtfs can import an extracted GTFS feed (issue #30)
* importgtfs defaults to a Feed name based on the agency name and start of
  service (issue #33)

0.4.1 (2014-07-11)
------------------
* Import GTFS feeds using BOM (issue #31)
* Export non-ASCII GTFS feeds in Python 2 (issue #34)
* Various admin improvements (issue #29, issue #32)

0.4.0 (2014-06-21)
------------------
This release was generously sponsored by MRCagney.

* Import and export are 17-21x faster.  Very large feeds (~20MB) can now be
  imported and exported without running out of memory (4 GB of RAM
  recommended).  When running management commands, increasing verbosity
  ('-v 1' or -v 2') will print useful status messages.
* Additional columns not in the current GTFS spec are now imported into
  'extra_data', a new JSON field.  The columns are noted in the Feed's new
  JSON field, 'meta'.  These addition items appear in the example project,
  and are exported after standard columns in the exported feed.
* Added Python 3 compatibility
* Extend more fields for real-world data (Trip.short_name,
  Zone.zone_id, and Block.block_id)
* On import, if two rows have duplicate unique ID (trip_id, stop_id, etc.),
  then only the first will be imported.  A warning will printed to stderr.
  Previously, both may have been imported, with unknown consequences.
* Dropped support for South 0.7.x (not Python 3 compatible)
* Trips now have a single Service.  Extra services will be detected by
  migration 0018, and will have to be manually removed.

0.3.3 (2014-03-28)
------------------
* Add new optional fields (issue #23):

  * trip.wheelchair_accessible
  * trip.bikes_allowed
  * stop.wheelchair_boarding

* Route.geometry does not include duplicate Trip.geometry lines (issue #24)
* Fix order of points in Shape.geometry (issue #25)
* Add management command 'refreshgeometries' to refresh cached geometries
  (useful if you were impacted by issues #24 or #25)

0.3.2 (2014-03-16)
------------------
This release was generously sponsored by MRCagney.

* Fix migration 0007 for PostGIS (issue #22)

0.3.1 (2014-03-12)
------------------
This release was generously sponsored by MRCagney.

* Add example project 'explore', which represents a feed as linked pages with
  OpenLayer maps.
* Add cached geometry for Routes, Trips, and Shapes.
* Extend fields for real-world data (FeedInfo.version, Route.short_name).
* Drop support for Points as geography fields.

0.3.0 (2014-02-01)
------------------
This release was generously sponsored by MRCagney.

* Convert to GeoDjango: Stops and ShapePoints use Points rather than lat/long,
  admin shows map of points, and new configuration settings to customize.
* Import south in try/except blocks (so that South really is optional).
* Django 1.5 or above is now required.

0.2.6 (2013-06-07)
------------------
* Remove verify_exists from URLField, so it can be used in Django 1.5

0.2.5 (2013-02-13)
------------------
* Human-friendly sorting for rest of GTFS output

0.2.4 (2013-02-06)
------------------
* Added optional manual sorting of output, used on stop_times.txt

0.2.3 (2012-11-09)
------------------
* Added South migrations for applying 0.2.2 changes

0.2.2 (2012-11-09)
------------------
* Fixed Fare.transfers for unlimited rides (use None instead of -1)
* First PyPi version
