#!/bin/sh
pg_dump --dbname=postgresql://devuser:devpassword@localhost:5434/web_app > ~/db.sql

# copy from DO to local
# scp root@nm:~/db.sql .

# to restore db

# stop web_app and exit from any app using it (such as pgadmin3)
# sudo docker-compose stop web_app

# drop db
# dropdb -h localhost -p 5434 -U devuser web_app

# load db
# psql -h localhost -p 5434 -U devuser web_app < db.sql