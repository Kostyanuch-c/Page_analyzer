#!/usr/bin/env bash


make install && export $(cat .env | xargs) && psql -a -d $DATABASE_URL -f database.sql