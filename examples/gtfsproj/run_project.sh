#!/bin/bash
set -e

# Create environment variables if not exist
ENVIRONMENT_FILE=".env"
if [ ! -f $ENVIRONMENT_FILE ]; then
  echo "Create default parameters using $ENVIRONMENT_FILE file"
  cp .env.example $ENVIRONMENT_FILE
fi

# If no arguments provided then run server on port 8000
if [ $# -eq 0 ]; then

  # If no arguments provided then run server on port 8000
  echo "Run development server on port 8000"
  exec ./manage.py runserver 0.0.0.0:8000

elif [ "$1" == "gunicorn" ]; then

  echo "Run gunicorn server on port 8000"
  exec gunicorn --bind 0.0.0.0:8000 gtfsproj.wsgi

else

  exec "$@"

fi
