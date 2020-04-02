"""
Django settings for fyle_xero_integration_web_app project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

import dj_database_url
from decouple import config
from django.conf.global_settings import DATABASES
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', config('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get('DEBUG', config('DEBUG')) == 'True' else False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', config('ALLOWED_HOSTS', default='')).split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'fyle_allauth',
    'apps.user',
    'apps.fyle_connect',
    'apps.xero_connect',
    'apps.xero_workspace',
    'apps.fyle_expense',
    'apps.task_log',
    'tempus_dominus',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fyle_xero_integration_web_app.urls'

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.filesystem.load_template_source',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'apps.user.context_processors.user_data',
                'apps.xero_workspace.context_processors.workspace_data',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fyle_xero_integration_web_app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES['default'] = dj_database_url.config(default=config('DATABASE_URL'))

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = 'media/'

# Set custom user model
AUTH_USER_MODEL = 'user.UserProfile'

# django-allauth settings
SITE_ID = 1
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/workspace'

# Using custom user model
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = os.environ.get('DEFAULT_HTTP_PROTOCOL', config('DEFAULT_HTTP_PROTOCOL'))

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

API_BASE_URL = os.environ.get('API_BASE_URL', config('API_BASE_URL'))

# Fyle Workspace OAuth2
FYLE_AUTHORISE_URI = os.environ.get('FYLE_AUTHORISE_URI', config('FYLE_AUTHORISE_URI'))
FYLE_CALLBACK_URI = os.environ.get('FYLE_CALLBACK_URI', config('FYLE_CALLBACK_URI'))
FYLE_TOKEN_URI = os.environ.get('FYLE_TOKEN_URI', config('FYLE_TOKEN_URI'))
FYLE_CLIENT_ID = os.environ.get('FYLE_CLIENT_ID', config('FYLE_CLIENT_ID'))
FYLE_CLIENT_SECRET = os.environ.get('FYLE_CLIENT_SECRET', config('FYLE_CLIENT_SECRET'))
FYLE_BASE_URL = os.environ.get('FYLE_BASE_URL', config('FYLE_BASE_URL'))
FYLE_JOBS_URL = os.environ.get('FYLE_JOBS_URL', config('FYLE_JOBS_URL'))

# Xero Workspace OAuth2
XERO_CLIENT_ID = os.environ.get('XERO_CLIENT_ID', config('XERO_CLIENT_ID'))
XERO_CLIENT_SECRET = os.environ.get('XERO_CLIENT_SECRET', config('XERO_CLIENT_SECRET'))
XERO_REDIRECT_URI = os.environ.get('XERO_REDIRECT_URI', config('XERO_REDIRECT_URI'))
XERO_SCOPE = os.environ.get('XERO_SCOPE', config('XERO_SCOPE'))
XERO_AUTHORIZE_URI = os.environ.get('XERO_AUTHORIZE_URI', config('XERO_AUTHORIZE_URI'))
XERO_TOKEN_URI = os.environ.get('XERO_TOKEN_URI', config('XERO_TOKEN_URI'))
XERO_BASE_URL = os.environ.get('XERO_BASE_URL', config('XERO_BASE_URL'))

MESSAGE_TAGS = {
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# SendGrid Email configuration
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', config('SENDGRID_API_KEY'))
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', config('SENDER_EMAIL'))

# Fyle Provider settings
SOCIALACCOUNT_PROVIDERS = {
    'fyle': {
        'APP': {
            'client_id': FYLE_CLIENT_ID,
            'secret': FYLE_CLIENT_SECRET,
        }
    }
}

# CORS
CORS_ORIGIN_ALLOW_ALL = True
