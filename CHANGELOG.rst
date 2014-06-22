Changelog
=========

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
    - trip.wheelchair_accessible
    - trip.bikes_allowed
    - stop.wheelchair_boarding
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

