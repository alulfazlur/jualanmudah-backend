#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&

source ~/.profile
echo "$DOCKER_PASSWORD" | docker login --username $DOCKER_USERNAME --password-stdin
docker stop slytherin
docker rm slytherin
docker rmi adul11/slytherin:latest
docker run -d --name slytherin -p 5050:5050 adul11/slytherin:latest
