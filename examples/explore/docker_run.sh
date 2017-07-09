#!/bin/bash

# Wait for PostgreSQL to be available
echo "Checking that PostgreSQL is running..."
until pg_isready -h db
do
    sleep 5
done

echo "Checking for DB explore..."
psql -lqt | cut -d \| -f 1 | grep -qw explore
if [ $? -ne 0 ]
then
    echo "  creating."
    CREATED=1
    createdb explore
    psql -d explore -c "CREATE EXTENSION postgis;"
    python ./manage.py migrate

    echo "Creating superuser admin with password 'password'"
    python ./manage.py createsuperuser --username admin --email admin@example.com --noinput
    echo "from django.contrib.auth.models import User; admin=User.objects.get(username='admin'); admin.set_password('password'); admin.save()" | python manage.py shell

    echo "Loading feeds"
    ls /feeds/import | grep -v "README.md" | xargs -I {} ./manage.py importgtfs /feeds/import/{}
else
    echo "  present!"
fi

python ./manage.py runserver_plus 0.0.0.0:8000
