#!/bin/sh
#Skrip ini akan membersihkan file migrasi dan membuat migrasi dari awal
#Jika proses ini bermasalah, hapus terlebih dahulu semua table dengan PgAdmin III

alembic downgrade base
rm -rf migrations/versions/*
alembic revision --autogenerate -m'initial db'
alembic upgrade head

python ./web_app/scripts/initdb.py
