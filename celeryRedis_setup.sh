#!/usr/bin/env bash


## Install Redis
sudo apt update
sudo apt install -y redis-server
## Start the Redis server
sudo systemctl start redis-server
## Enable Redis to start on boot
sudo systemctl enable redis-server
## install celery
pip install celery[redis]

## starting celery
# celery -A celery_config worker --loglevel=info
