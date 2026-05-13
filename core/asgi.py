"""
CORE CONFIGURATION - ASGI
-------------------------
This file exposes the ASGI callable as a module-level variable named ``application``.
ASGI is the asynchronous version of WSGI, used for Real-time features (WebSockets).
"""
import os

from django.core.asgi import get_asgi_application

# Points to the development settings by default.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.dev')

application = get_asgi_application()
