#!/usr/bin/env bash

# Exit on error
set -o errexit

# Navigate to the backend directory where manage.py is located
# cd waypik_backend

pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --noinput

# Apply any outstanding migrations
python manage.py migrate --noinput

# Create superuser if it doesn't exist
# We use a python script to safely check for existence first
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
import os

User = get_user_model()
PHONE = os.environ.get('SUPERUSER_PHONE', '0000000000') # Default or from env
PASSWORD = os.environ.get('SUPERUSER_PASSWORD', 'admin123')

if not User.objects.filter(phone=PHONE).exists():
    print(f"Creating superuser {PHONE}...")
    User.objects.create_superuser(phone=PHONE, password=PASSWORD)
else:
    print(f"Superuser {PHONE} already exists.")
EOF