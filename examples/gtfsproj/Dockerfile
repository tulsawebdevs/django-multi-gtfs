FROM python:3

# Install system dependencies
RUN apt-get update && apt-get install -y \
  binutils \
  gdal-bin \
  libproj-dev \
  postgresql-client

# Copy project code (current folder)
COPY . /code

# Install project dependencies, please note uses
# pypi version of gtfsmulti not local version.
# NB: To use local you will need to copy multigtfs 
# code to image and update requirements.txt
WORKDIR /code
RUN pip install -r requirements.txt

# Create volume for feeds
VOLUME /gtfs/feeds

# run_project script passes all arguments except
# bash to django manage.py script for project
# runs development server by default
RUN chmod +x /code/run_project.sh
ENTRYPOINT ["/code/run_project.sh"]
CMD ["./manage.py", "runserver", "0.0.0.0:8000"]
