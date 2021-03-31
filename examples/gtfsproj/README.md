<h1>Multi GTFS project</h1>

This is an alternative example project. It is largely based on the 
"explore" example project but has been recreated with slightly different
structure. 

The intention is that this example will ultimately provide a  
slightly different experience. This will include more mapping (possibly
using leaflet), new template (e.g. bootstrap 4) and different navigation.

<h2>Run with Docker</h2>

<h3>Build and run</h3>

Build docker image. This will use the settings in teh .env.example
file, which can be replaced by creating a ".env" file before building
the image (eg. cp env.example .env).

    # Get source code
    git clone https://github.com/alaw005/django-multi-gtfs.git
    cd django-multi-gtfs/examples/gtfsproj

    # Build image
    sudo docker build -t multiproj .

Run docker container as background (to run in forground change 
"-d" to "-it". This will automatically run the development server 
using the settings in the .env.example file.

    # Create container
    sudo docker run -d -p 8000:8000 --name multiproj1 multiproj

Now setup database and superuser, refer management commands below.
This is only required if database does not already exist or multgtfs
has been updated (in which case need to migrate only)

    # Setup database (if required)
    sudo docker exec -it multiproj1 ./manage.py migrate
    sudo docker exec -it multiproj1 ./manage.py createsuperuser

Now you can access from browser using host IP address and port 8000.

<h3>Management commands</h3>

You can run django management commands as follows:

    sudo docker exec -it multiproj1 ./manage.py help

For example, to load a new feed you can do the following (assuming 
container name is "multiproj1"). NB: The first command copies a 
file from host system to the container. 

    cat /host/feeds/feed.zip | sudo docker exec -i multiproj1 sh -c 'cat > /gtfs/feeds/feed.zip'
    sudo docker exec -it multiproj1 ./manage.py importgtfs /gtfs/feeds/feed.zip

To specify a feed name rather than the defaul use the following.

    sudo docker exec -it multiproj1 ./manage.py importgtfs --name "Feed name" /feeds/feed.zip

<h3>Creating postgres database (assumes server already running)</h3>

At the command line (as long as postgres is installed):

    # Create database
    createdb -h HOST -p 5432 -U USERNAME multigtfs

    # Install postgis extension
    psql -h HOST -p 5432 -U USERNAME -d multigtfs -c "CREATE EXTENSION postgis;"

Now initiatise the database using multigtfs:

	# Configure database
    sudo docker exec -it multigtfs ./manage.py migrate

    # Create superuser
    sudo docker exec -it multigtfs ./manage.py createsuperuser

That's it.

<h2>Run without Docker</h2>

The following applies to Ubunutu

    sudo apt-get install -y git python-pip python-virtualenv spatialite-bin gdal-bin
 
    cd ~/
    git clone https://github.com/alaw005/django-multi-gtfs.git
 
    # Navigate to project folder
    cd django-multi-gtfs/examples/multiproj
 
    # Create and activate new virtual environment (myenv). 
    # Use "deactivate" to deactivate virtualenv.
    virtualenv --always-copy myenv
    source myenv/bin/activate
 
    pip install -r requirements.txt
 
    # Create multigtfs tables in database
    ./manage.py migrate
 
    # Create db.sqlite3, superuser. Enter "yes" to create superuser and 
    # then enter username and password when prompted (you can leave email address blank)
    ./manage.py createsuperuser
 
    # Run
    ./manage.py runserver 0.0.0.0:8000

Now you can access from browser using host IP address and port 8000.

<h2>Environment variables</h2>

You can either set environment variables in the .env file as per above or directly
at command line when you create the container. For example, to use existing postgis database:

    sudo docker run -d -p 8000:8000 --name multiproj1 -e DATABASE_URL=postgis://USER:PASSWORD@HOST:PORT/DBNAME  multiproj

The environment variables you can change are identified in the following file:

    django-multi-gtfs/examples/gtfsproj/gtfsproj/settings.py

They all use the config() function e.g. SECRET_KEY is set in the following example,
indicated by the "config('SECRET_KEY'" section.

    SECRET_KEY = config('SECRET_KEY', default='+$8pgzf)luxklr(rhzg4!$6+b^2hbw*-frvh_2-7an9-_==n_u', cast=str)


