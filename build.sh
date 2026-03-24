#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Build Tailwind CSS (adjust if your build command is different)
npm run build

# Collect static files for Django
python manage.py collectstatic --noinput

python manage.py migrate
