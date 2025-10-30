# Paste in: illinois/settings/development.py

# We will first import everything from base.py (our new settings.py file that we renamed to base.py)
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']