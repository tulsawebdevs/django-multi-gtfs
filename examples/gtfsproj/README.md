
Build docker image.

    sudo docker build -t multiproj .

Run docker container as background (to run in forground change 
"-d" to "-it".

    sudo docker run -d -p 8000:8000 --name multiproj1 multiproj

