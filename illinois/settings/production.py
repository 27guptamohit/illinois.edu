# Paste in: illinois/settings/production.py

# We will first import everything from base.py (our new settings.py file that we renamed to base.py)
from .base import *

DEBUG = False

# Enter your PythonAnywhere account here in the allowed hosts.
# Replace it with your name:
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'mohitg2.pythonanywhere.com']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "mohitg2$info390mg-mysql-database",
        "USER": "mohitg2",
        "PASSWORD": "graingerlibrary",
        "HOST": "mohitg2.mysql.pythonanywhere-services.com",
        "PORT": "3306",
    }
}

