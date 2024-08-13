#!/usr/bin/env bash

## Reload the systemd daemon to recognize the new service
sudo systemctl daemon-reload

## Start the Celery worker service
sudo systemctl start celery-worker

## Enable the service to start on boot
sudo systemctl enable celery-worker

## Check celery-worker status
sudo systemctl status celery-worker
