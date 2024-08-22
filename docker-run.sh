#!/bin/bash

docker compose -f docker-compose.local.yml run django $@
