#!/usr/bin/env bash
# Para tudo se algum comando falhar
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate