from .base import *

DEBUG = False

# Security settings for production
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True') == 'True'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# For Render/Gunicorn
ALLOWED_HOSTS = [
    '*',
    '.onrender.com',
]
