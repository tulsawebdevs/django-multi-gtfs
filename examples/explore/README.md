# Example Project - GTFS Explorer

This project lets you explore GTFS data in a web interface.  It should
demonstrate how to use django-multi-gtfs in your own projects.

## Requirements

This project uses [spatiallite][spatialite] by default.  You'll need to
[install the spatialite tools][sp_tut] on your system.

If you want to use an alternate database
(e.g. [PostGIS][postgis]), you can create an alternate `DATABASES`
definition in `exploreproj/local_settings.py`, and adjust the installation
accordingly.

## Installation

    $ cd /path/to/explore
    $ mkvirtualenv explore             # Create a virtual environment
    $ pip install -r requirements.txt  # Install Django, etc.
    $ ./manage.py syncdb               # Create db.sqlite3, superuser
    $ ./manage.py migrate              # Add multigtfs tables
    $ ./manage.py runserver            # Run on http://localhost:8000

[postgis]: http://boundlessgeo.com/solutions/solutions-software/postgis/ "PostGIS homepage"
[spatialite]: https://www.gaia-gis.it/fossil/spatialite-tools/index "spatialite-tools homepage"
[sp_tut]: http://www.gaia-gis.it/gaia-sins/spatialite-tutorial-2.3.1.html "SpatiaLite tutorial"
