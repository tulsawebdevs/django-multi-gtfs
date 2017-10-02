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
  exec ./manage.py runserver 0.0.0.0:8000
else
  if [ $1 = "bash" ]; then
    # If bash first argument then use that for all arguments
    exec "$@"
  else
    # Otherwise pass arguments to django manage.py script
    exec ./manage.py "$@"
  fi
fi

