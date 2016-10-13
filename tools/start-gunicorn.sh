#! /bin/bash

cd $(dirname $0)/..
. tools/export_env.sh local
gunicorn app.wsgi:application --conf gunicorn.conf --bind localhost:8000
