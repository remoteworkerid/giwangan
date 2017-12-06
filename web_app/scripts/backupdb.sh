#!/bin/sh
pg_dump --dbname=postgresql://devuser:devpassword@localhost:5434/web_app > ~/db.sql