FROM python:3

# Install system dependencies
RUN apt-get update && apt-get install -y \
  binutils \
  gdal-bin \
  libproj-dev \
  postgresql-client

# Copy project code (current folder)
COPY . /code

# Install project dependencies
WORKDIR /code
RUN pip install -r requirements.txt

# Create volume for feeds
VOLUME /gtfs/feeds

CMD ["/bin/bash"]

