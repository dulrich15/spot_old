import os.path
import random

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_NAME = PROJECT_PATH.split(os.path.sep)[-1]

MY_APPS = (
    'classroom',
#     'docmaker',
#     'gradebook',
#     'mindmap',
)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'spot.db',
    },
}

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = True
USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')    # used to hold user uploads

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')  # used for collecstatic command in production
STATICFILES_FINDERS = (                             # used for staticfiles app in development
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_DIRS = ()                               # extra folders for staticfiles app

if not hasattr(globals(), 'SECRET_KEY'):
    secret_file = os.path.join(PROJECT_PATH, 'local', 'secret_key.txt')
    try:
        SECRET_KEY = open(secret_file).read().strip()
    except IOError:
        try:
            chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
            SECRET_KEY = ''.join([random.choice(chars) for i in range(50)])

            LOCAL_PATH = os.path.join(PROJECT_PATH, 'local')
            if not os.path.isdir(LOCAL_PATH):
                os.mkdir(LOCAL_PATH)

            secret = file(secret_file, 'w')
            secret.write(SECRET_KEY)
            secret.close()
        except IOError:
            raise Exception('Please create file %s filled with random characters'
                            ' to serve as your secret key.' % secret_file)
    del secret_file

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'website.urls'

WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'website', 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'south',
    'website',
)

for app in MY_APPS:
    INSTALLED_APPS += ('apps.{}'.format(app),)
    
# TEX_PATH   = r'/home/dulrich/texlive/bin/i386-linux'
# GS_CMD     = r'/usr/bin/gs'
# PYTHON_CMD = r'python2.7'

try:
    from local.settings import *
except ImportError:
    pass
