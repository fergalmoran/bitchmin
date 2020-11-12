#!/usr/bin/env bash

docker run -d \
    --name bitchmin-postgres \
    -e POSTGRES_PASSWORD=postgres \
    -p 5432:5432 \
    -e /home/fergalm/dev/BitchMin/bitchmin-api/.working/pgdata=/var/lib/postgresql \
    -d library/postgres

docker exec -it bitchmin-postgres psql \
  -U postgres \
  -c "CREATE DATABASE bitchmin;"

docker exec -it bitchmin-postgres psql \
  -U postgres \
  -c "CREATE USER bitchmin WITH PASSWORD 'bitchmin';"

docker exec -it bitchmin-postgres psql \
  -U postgres \
  -c "grant all privileges on database bitchmin to bitchmin;"


