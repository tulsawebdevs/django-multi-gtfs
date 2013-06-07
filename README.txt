django-multi-gtfs - The General Transit Feed Specification (GTFS) in Django

Developed for the Tulsa Web Dev's project to get Tulsa's buses into Google
Maps.  Allows storage of multiple independent GTFS feeds, for combining or
versioning.

To run app tests:
* Create a virtualenv (I recommend virtualenvwrapper)
* pip install -r requirements.txt
* pip install -r requirements.dev.txt
* ./qa_check.sh

Once you've added multigtfs to your INSTALLED_APPS, you can use two management
commands to get feeds in and out of the database:

    ./manage.py importgtfs [--name name_of_feed] path/to/gtfsfeed.zip
    ./manage.py exportgtfs [--name basename_of_file] <feed_id>

See http://tulsawebdevs.org for more information about the project.
