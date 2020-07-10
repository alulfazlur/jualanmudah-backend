#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&

source ~/.profile
echo "$DOCKER_PASSWORD" | docker login --username $DOCKER_USERNAME --password-stdin
sudo docker stop slytherin
sudo docker rm slytherin
sudo docker rmi adul11/slytherin:latest
sudo docker run -d --name slytherin -p 5050:5050 adul11/slytherin:latest
