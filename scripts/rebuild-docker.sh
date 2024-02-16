#!/bin/bash

docker-compose stop backend_server
docker-compose rm backend_server
docker rmi hacku-2024-myj-backend-server
docker-compose build --no-cache
