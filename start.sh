#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

python /app/manage.py migrate

uwsgi --ini /app/uwsgi.ini

