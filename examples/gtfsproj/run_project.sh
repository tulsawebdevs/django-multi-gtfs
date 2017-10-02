#!/bin/bash

# Create environment variables if not exist
ENVIRONMENT_FILE=.env2
if [ ! -f $ENVIRONMENT_FILE ]; then
    echo "Create default environment from example"
    cp .env.example $ENVIRONMENT_FILE
fi

./manage.py runserver 0.0.0.0:8000
