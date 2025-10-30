# illinois/settings/base.py

from pathlib import Path

# 1) BASE DIR
# this brings you from:
#   illinois/illinois/settings/base.py
# → illinois.edu/   (project root, where manage.py is)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 2) CORE
SECRET_KEY = 'django-insecure-tf=3n&lfpj7@ab4@8$q1tncl05auel#e2uluyh+rdmwj5^@wd$'
DEBUG = True
ALLOWED_HOSTS = []

# 3) APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'students',
]

# 4) MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'illinois.urls'

# 5) TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # you have illinois.edu/templates/
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'illinois.wsgi.application'

# 6) DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # put the DB in project-root/data/db.sqlite3
        'NAME': BASE_DIR / 'data' / 'db.sqlite3',
    }
}

# 7) AUTH VALIDATORS
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 8) I18N
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 9) STATIC
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# static for (the build output)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 10) DEFAULT PK
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 11) AUTH REDIRECTS
LOGIN_URL = 'login_urlpattern'
LOGIN_REDIRECT_URL = 'student-list-url'
LOGOUT_REDIRECT_URL = 'login_urlpattern'






















