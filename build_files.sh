#!/bin/bash
echo "Building project packages..."
python3 -m pip install -r requirements.txt
echo "Migrating Database..."
python3 manage.py migrate
echo "Collecting static files..."
python3 manage.py collectstatic --noinput --clear
echo "Seeding initial clinic data..."
python3 manage.py seed_data
