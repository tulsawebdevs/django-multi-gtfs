django-multi-gtfs - The General Transit Feed Specification (GTFS) in Django

Developed for the Tulsa Web Dev's project to get Tulsa's buses into Google
Maps.  Allows storage of multiple independent GTFS feeds, for combining or
versioning.

To run app tests:
* Install spatialite (see
  <https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/spatialite/>)
* Create a virtualenv (I recommend virtualenvwrapper)
* pip install -r requirements.txt
* pip install -r requirements.dev.txt
* ./qa_check.sh

For development and production, I recommend PostgreSQL 9.x and PostGIS 2.x.
This will support all of the features of GeoDjango.

Once you've added multigtfs to your INSTALLED_APPS, you can use two management
commands to get feeds in and out of the database:

    ./manage.py importgtfs [--name name_of_feed] path/to/gtfsfeed.zip
    ./manage.py exportgtfs [--name basename_of_file] <feed_id>

See http://tulsawebdevs.org for more information about the project.
