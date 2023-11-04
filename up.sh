#!/bin/bash

# environment
set -a
source .env

# start
docker compose -f $(ls docker-compose*.yml | awk '{printf "-f %s ", $0}') up -d