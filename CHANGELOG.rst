Changelog
=========

0.3.0 (2014-02-01)
------------------
This release was sponsored by MRCagney_.
* Convert to GeoDjango support


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

.. _MRCagney: http://mrcagney.co.nz
