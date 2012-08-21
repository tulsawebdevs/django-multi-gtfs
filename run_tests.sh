#!/bin/bash
PYTHONPATH=$PWD/src/${PYTHONPATH:+:$PYTHONPATH}
export PYTHONPATH
echo $PYTHONPATH

echo "Running django-multi-gtfs tests..."
django-admin.py test multigtfs --settings=multigtfs.tests.settings

