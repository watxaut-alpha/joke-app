#!/bin/bash

# stop all containers
docker stop $(shell docker ps -q -a)

# pull last changes from master
git checkout master
git pull

# build new docker image
docker build -t jokes-app:0.2.0 .

# Run new container
docker run -it --rm --name jokes-app-docker jokes-app:0.2.0