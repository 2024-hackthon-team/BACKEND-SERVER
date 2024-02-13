#!/bin/bash

docker-compose down
docker rmi hacku-2024-myj-backend-server
docker-compose build --no-cache
