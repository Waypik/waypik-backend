"""
CORE CONFIGURATION - WSGI
-------------------------
This file exposes the WSGI callable as a module-level variable named ``application``.
It is used by production web servers (like Gunicorn) to serve your project.
"""
import os

from django.core.wsgi import get_wsgi_application

# Points to the development settings by default. 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.dev')

application = get_wsgi_application()
