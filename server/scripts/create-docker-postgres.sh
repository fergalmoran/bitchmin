#!/usr/bin/env bash

docker run  -e POSTGRES_PASSWORD=docker  library/postgres


docker run -d \
    --name bitchmin-postgres \
    -e POSTGRES_PASSWORD=postgres \
    -p 5432:5432 \
    -e /opt/postgres/bitchmin=/var/lib/postgresql/data \
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

kubectl exec -it postgres-5f4895b95d-4xz92 \
  'psql -U postgres -c "CREATE DATABASE bitchmin;"'

kubectl exec -it postgres-5f4895b95d-4xz92 \
 "psql -U postgres -c $"CREATE USER bitchmin WITH PASSWORD \'bitchmin\';'"

psql -U postgres -c 'psql -c "CREATE USER bitchmin WITH PASSWORD '\''bitchmin'\'';"'

kubectl exec -it postgres-5f4895b95d-4xz92 \
  'psql -U postgres -c "grant all privileges on database bitchmin to bitchmin;"'
su - postgres -c 'psql -c "grant all privileges on database bitchmin to bitchmin;"'



# DATABASE_URL='postgresql+psycopg2://bitchmin:bitchmin@10.1.1.1/bitchmin'
# psql postgres -c "CREATE DATABASE BitchMin WITH ENCODING 'UTF8'
