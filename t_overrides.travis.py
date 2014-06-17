# Copy to test_overrides.py, make changes

import os


def update(old_config):
    config = old_config.copy()

    if os.environ.get('MULTIGTFS_TEST_POSTGIS', False):
        # Run tests under PostgreSQL / PostGIS
        # Requires psycopg2:
        #    pip install psycopg2
        # Requires the PostgreSQL role with SUPERUSER and CREATEDB permission
        #    createuser multigtfs --superuser --createdb --pwprompt
        # Requires the PostgreSQL database w/ PostGIS extensions:
        #    createdb multigtfs --owner=multigtfs
        #    psql -d multigtfs -c "CREATE EXTENSION postgis"
        #    psql -d multigtfs -c "CREATE EXTENSION postgis_topology"
        # Running the test creates a new database 'test_multigtfs'
        # Because superuser permissions are needed, it is recommended that you
        #  only install on a local database, and change configuration items
        #  below.
        config['DATABASE_ENGINE'] = 'django.contrib.gis.db.backends.postgis'
        config['DATABASES'] = {
            'default': {
                'ENGINE': 'django.contrib.gis.db.backends.postgis',
                'NAME': 'multigtfs',
                'USER': 'postgres'}}
    return config
