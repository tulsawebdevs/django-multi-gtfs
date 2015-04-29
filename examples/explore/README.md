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

### Detailed installation instructions

The following steps have been used to install the example project onto a clean Ubuntu (virtual) machine. The only prerequesite is that Python 2.7 is installed. This process should also work in Windows with minor tweaks.

Step 1 - Install operating system dependencies

    sudo apt-get install -y git python-pip python-virtualenv spatialite-bin gdal-bin

Step 2 - Download copy of multigtfs from git into project folder (assume home directory)

    cd ~/
    git clone https://github.com/tulsawebdevs/django-multi-gtfs.git
    
Step 3 - Navigate to example project folder and create python virtual environment (myenv) for example project (use command "deactivate" to deactivate virtualenv).  

    # Navigate to example project folder
    cd django-multi-gtfs/examples/explore
    
    # Create and activate new virtual environment (myenv). Use "deactivate" to deactivate virtualenv.
    virtualenv --always-copy myenv
    source myenv/bin/activate

Step 4 - Install example project dependencies (django etc)

    sudo pip install -r requirements.txt
	
Step 5 - Setup multigtfs application/database etc.

    # Create db.sqlite3, superuser. Enter "yes" to create superuser and 
    # then enter username and password when promted (you can lease email address blank)
    ./manage.py syncdb
    
    # Create multigtfs tables in database
    ./manage.py migrate
    
Step 6 - Example project now installed, run development server to test. Note I have used 0.0.0.0:8000 so can can access from any computer on network (not use host). This is necessary if running in a virtual machine (along with appropriate network settiings/port forwarding, for example in my virtual machine Vagrantfile I use  config.vm.network "public_network" to allow access from other machines)

    ./manage.py runserver 0.0.0.0:8000
    
Done. The multigtfs server should now be running. Open your favourate web browser and enter the following to access the application (use appropriate IP address if browser not on same machine, you can use ifconfig in Ubuntu to get IP address).

    http://localhost:8000

At this stage there are no GTFS feeds defined so lets add one. Return to the command line and enter Control-C to return to stop server. The following steps download the latest Wellington Metlink GTFS feed from http://www.gtfs-data-exchange.com/.

	# Download a GTFS feed
	wget -O wellington-metlink-latest.zip http://www.gtfs-data-exchange.com/agency/metlink/latest.zip

	# Import into GTFS
	./manage.py importgtfs --name "Wellington Metlink latest" wellington-metlink-latest.zip

	# Delete download
	rm wellington-metlink-latest.zip

Note that the importgtfs process will take some time. When compelte start the multigtfs server again and the new feed should not be available.
	


