"""
Django settings for danesh_boom project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from danesh_boom.settings_helpers import get_config, get_db_settings

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from danesh_boom.social_auth_pipeline import LOCAL_SOCIAL_AUTH_PIPELINE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG = get_config(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.get('DEBUG')

ALLOWED_HOSTS = CONFIG.get('ALLOWED_HOSTS')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'pages',
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

ROOT_URLCONF = 'danesh_boom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

WSGI_APPLICATION = 'danesh_boom.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': get_db_settings(CONFIG)
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

if CONFIG.get('EMAIL').get('ENABLE_SMTP'):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = CONFIG.get('EMAIL').get('HOST')
EMAIL_HOST_USER = CONFIG.get('EMAIL').get('HOST_USER')
EMAIL_HOST_PASSWORD = CONFIG.get('EMAIL').get('HOST_PASSWORD')
EMAIL_PORT = CONFIG.get('EMAIL').get('PORT')
EMAIL_USE_TLS = CONFIG.get('EMAIL').get('USE_TLS')
EMAIL_FROM = CONFIG.get('EMAIL').get('EMAIL_FROM')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

FRONTEND_DEV = CONFIG.get('FRONTEND_DEV')
FRONTEND_STATIC = CONFIG.get('FRONTEND_STATIC')

if FRONTEND_DEV:
    STATIC_URL = 'http://localhost:3000/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, FRONTEND_STATIC),
]
STATIC_ROOT = os.path.join(BASE_DIR, CONFIG.get('STATIC_ROOT'))

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = CONFIG.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = CONFIG.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_PIPELINE = LOCAL_SOCIAL_AUTH_PIPELINE
