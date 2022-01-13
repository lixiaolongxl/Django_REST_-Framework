#!/bin/bash

docker-compose stop

yes | docker-compose rm

docker rmi app_web:latest

sudo docker-compose build


sudo docker-compose up -d

docker ps
