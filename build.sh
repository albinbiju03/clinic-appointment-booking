#!/usr/bin/env bash
# exit on error
set -o errexit

python -m pip install --upgrade pip
python -m pip install pipenv

python -m pipenv install --system

# Force install required production packages to bypass Pipenv lock issues
python -m pip install Pillow gunicorn whitenoise

python manage.py collectstatic --no-input
python manage.py migrate