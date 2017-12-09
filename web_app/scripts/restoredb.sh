#!/bin/sh
# copy from DO to local
# scp root@nm:~/db.sql .

# stop web_app and exit from any app using it (such as pgadmin3)
sudo docker-compose stop web_app

# drop db
dropdb -h localhost -p 5434 -U devuser web_app

# create db
createdb -h localhost -p 5434 -U devuser web_app

# load db
psql -h localhost -p 5434 -U devuser web_app < db.sql

# start web_app
sudo docker-compose start web_app