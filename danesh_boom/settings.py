"""
Django settings for danesh_boom project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import datetime
import datetime
import os

from django.utils.translation import ugettext_lazy as _

from danesh_boom.settings_helpers import get_config, get_db_settings, load_static_asset_manifest
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
    'graphene_django',
    'base',
    'users',
    'organizations',
    'media',
    'products',
    'chats',
    'exchanges',
    'forms',
    'displacements',
    'rest_framework',
    'rest_framework.authtoken',
    'social_django',
    'rest_social_auth',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'users.views.jwt_response_payload_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=30),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7)
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '50/min',
        'user': '100/min'
    }
}

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
                'users.context_processors.static',

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.linkedin.LinkedinOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.instagram.InstagramOAuth2',
    'social_core.backends.yahoo.YahooOAuth2',
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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

CACHE_TIMEOUT = 60 * 60 * 24

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGE_SESSION_KEY = 'LANG'
LANGUAGES = [
    ('fa', _('Persian')),
    ('en', _('English')),
]
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]
TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

if CONFIG.get('EMAIL').get('ENABLE_SMTP'):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
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
FRONTEND_ROOT = os.path.join(BASE_DIR, CONFIG.get('FRONTEND_ROOT'))
FRONTEND_BUILD_ROOT = os.path.join(
    FRONTEND_ROOT, CONFIG.get('FRONTEND_BUILD_ROOT'))

STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, 'static'),
]
# STATIC_ROOT = os.path.join(BASE_DIR, CONFIG.get('STATIC_ROOT'))

STATIC_ASSET_MANIFEST = load_static_asset_manifest(
    FRONTEND_BUILD_ROOT, FRONTEND_DEV)

'''SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = CONFIG.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = CONFIG.get(
    'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_PIPELINE = LOCAL_SOCIAL_AUTH_PIPELINE
SOCIAL_AUTH_RAISE_EXCEPTIONS = False'''


SOCIAL_AUTH_GITHUB_KEY = '67a98bf8d7882de6ce0f'
SOCIAL_AUTH_GITHUB_SECRET = '753ee8b506b04f338f1b38234f4f05b30fbd2e4a'


LOGIN_URL = '/login'
LOGOUT_URL = '/logout'
LOGIN_REDIRECT_URL = '/home'

GRAPHENE = {
    'SCHEMA': 'danesh_boom.schema.schema',
    'SCHEMA_OUTPUT': os.path.join(
        BASE_DIR,
        FRONTEND_ROOT,
        'graphql.schema.json'),
}

# x-sendfile
SENDFILE_BACKEND = CONFIG.get('SENDFILE_BACKEND')
SENDFILE_ROOT = os.path.normpath(
    os.path.join(
        BASE_DIR,
        CONFIG.get('SENDFILE_ROOT')))
SENDFILE_URL = CONFIG.get('SENDFILE_URL')
# not MEDIA_ROOT. this is media app settings
MEDIA_DIR = os.path.join(SENDFILE_ROOT, 'media')

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

SOCIAL_AUTH_FACEBOOK_KEY = CONFIG.get('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = CONFIG.get('SOCIAL_AUTH_FACEBOOK_SECRET')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', ]  # optional

SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = CONFIG.get('SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY')
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = CONFIG.get('SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET')
SOCIAL_AUTH_LINKEDIN_OAUTH2_REDIRECT_URI = CONFIG.get('SOCIAL_AUTH_LINKEDIN_OAUTH2_REDIRECT_URI')
# Add email to requested authorizations.
SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_basicprofile', 'r_emailaddress']
# Add the fields so they will be requested from linkedin.
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = ['email-address', 'headline', 'industry']
# Arrange to add the fields to UserSocialAuth.extra_data
SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [('id', 'id'),
                                          ('firstName', 'first_name'),
                                          ('lastName', 'last_name'),
                                          ('emailAddress', 'email_address'),
                                          ('headline', 'headline'),
                                          ('industry', 'industry')]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = CONFIG.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = CONFIG.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

SOCIAL_AUTH_INSTAGRAM_KEY = CONFIG.get('SOCIAL_AUTH_INSTAGRAM_KEY')
SOCIAL_AUTH_INSTAGRAM_SECRET = CONFIG.get('SOCIAL_AUTH_INSTAGRAM_SECRET')

SOCIAL_AUTH_YAHOO_OAUTH2_KEY = CONFIG.get('SOCIAL_AUTH_YAHOO_OAUTH2_KEY')
SOCIAL_AUTH_YAHOO_OAUTH2_SECRET = CONFIG.get('SOCIAL_AUTH_YAHOO_OAUTH2_SECRET')

# SOCIAL_AUTH_PIPELINE = LOCAL_SOCIAL_AUTH_PIPELINE
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'danesh_boom.pipeline.log'
)

SOCIAL_AUTH_RAISE_EXCEPTIONS = False

EXCHANGE_LIMIT = 100

TAG_KEY_MAPPING = {
    'TY': 'type_of_reference',
    'A1': 'first_authors',  # ListType
    'A2': 'secondary_authors',  # ListType
    'A3': 'tertiary_authors',  # ListType
    'A4': 'subsidiary_authors',  # ListType
    'AB': 'abstract',
    'AD': 'author_address',
    'AN': 'accession_number',
    'AU': 'authors',  # ListType
    'C1': 'custom1',
    'C2': 'custom2',
    'C3': 'custom3',
    'C4': 'custom4',
    'C5': 'custom5',
    'C6': 'custom6',
    'C7': 'custom7',
    'C8': 'custom8',
    'CA': 'caption',
    'CN': 'call_number',
    'CY': 'place_published',
    'DA': 'date',
    'DB': 'name_of_database',
    'DO': 'doi',
    'DP': 'database_provider',
    'ET': 'edition',
    'EP': 'end_page',
    'ID': 'id',
    'IS': 'number',
    'J2': 'alternate_title1',
    'JA': 'alternate_title2',
    'JF': 'alternate_title3',
    'JO': 'journal_name',
    'KW': 'keywords',  # ListType
    'L1': 'file_attachments1',
    'L2': 'file_attachments2',
    'L4': 'figure',
    'LA': 'language',
    'LB': 'label',
    'M1': 'note',
    'M3': 'type_of_work',
    'N1': 'notes',  # ListType
    'N2': 'abstract',
    'NV': 'number_of_Volumes',
    'OP': 'original_publication',
    'PB': 'publisher',
    'PY': 'year',
    'RI': 'reviewed_item',
    'RN': 'research_notes',
    'RP': 'reprint_edition',
    'SE': 'version',
    'SN': 'issn',
    'SP': 'start_page',
    'ST': 'short_title',
    'T1': 'primary_title',
    'T2': 'secondary_title',
    'T3': 'tertiary_title',
    'TA': 'translated_author',
    'TI': 'title',
    'TT': 'translated_title',
    'UR': 'url',
    'VL': 'volume',
    'Y1': 'publication_year',
    'Y2': 'access_date',
    'ER': 'end_of_reference',
    'UK': 'unknown_tag',
}

ORGANIZATION_RELATED_MODELS_ACTIONS = (
    ('add-exchange', ' افزودن بورس '),
    ('edit-exchange', ' ویرایش بورس '),
    ('delete-exchange', ' حذف بورس '),
    ('add-product', ' افزودن محصول '),
    ('edit-product', ' ویرایش محصول '),
    ('delete-product', ' حذف محصول '),
)

# Displacement Data Settings
LAST_DATABASE_NAME = 'danesh_boom3'
LAST_DATABASE_USERNAME = 'postgres'
LAST_DATABASE_PASSWORD = '1A2b3F4po'

USERS_BEFORE_FIELDS = {
    'id': '',
    'username': '',
    'password': '',
    'first_name': '',
    'last_name': '',
    'email': '',
    'date_joined': '',
    'is_staff': '',
    'is_active': ''
}

PROFILES_BEFORE_FIELDS = {
    'public_email': '',
    'national_code': '',
    'profile_media_id': '',
    'birth_date': '',
    'web_site': '',
    'phone': '',
    'mobile': '',
    'fax': '',
    'telegram_account': '',
    'description': '',
}

IDENTITY_BEFORE_FIELDS = {
    'identity_organization_id': '',
    'name': ''
}

CATEGORY_BEFORE_FIELDS = {
    'base_ptr_id': '',
    'category_parent_id': '',
    'name': '',
    'title': '',
    'creatable': ''
}

CATEGORY_FIELDS_BEFORE_FIELDS = {
    'base_ptr_id': '',
    'field_category_id': '',
    'name': '',
    'title': '',
    'type': '',
    'order': '',
    'option': ''
}

PRODUCTS_BEFORE_FIELDS = {
    'base_ptr_id': '',
    'product_owner_id': '',
    'product_category_id': '',
    'name': '',
    'country': '',
    'province': '',
    'city': '',
    'description': '',
    'attrs': '',
    'custom_attrs': ''
}

PRICES_BEFORE_FIELDS = {
    'base_ptr_id': '',
    'price_product_id': '',
    'value': ''
}

COMMENTS_BEFORE_FIELDS = {
    'base_ptr_id': '',
    'comment_product_id': '',
    'comment_user_id': '',
    'text': ''
}

ORGANIZATION_BEFORE_FIELDS = {
    'base_ptr_id': '',
    'owner_id': '',
    'username': '',
    'email': '',
    'nike_name': '',
    'official_name': '',
    'national_code': '',
    'registration_ads_url': '',
    'registrar_organization': '',
    'country': '',
    'province': '',
    'city': '',
    'address': '',
    'phone': '',
    'web_site': '',
    'established_year': '',
    'ownership_type': '',
    'business_type': '',
    'organization_logo_id': '',
    'biography': '',
    'description': '',
    'correspondence_language': '',
    'social_network': '',
    'staff_count': ''
}

STAFF_COUNT_BEFORE_FIELDS = {
    'base_ptr_id': '',
    'staff_count_organization_id': '',
    'count': ''
}

STAFF_BEFORE_FIELDS = {
    'base_ptr_id': '',
    'staff_organization_id': '',
    'staff_user_id': '',
    'position': '',
    'post_permission': ''
}

ABILLITY_BEFORE_FIELDS = {
    'ability_organization_id': '',
    'title': '',
    'text': ''
}

CUSTOMER_BEFORE_FIELDS = {
    'customer_organization_id': '',
    'related_customer_id': '',
    'title': '',
    'customer_picture_id': ''
}

CONFIRMATION_BEFORE_FIELD = {
    'confirmation_corroborant_id': '',
    'confirmation_confirmed_id': '',
    'title': '',
    'description': '',
    'link': '',
    'confirm_flag': ''
}

FOLLOW_BEFORE_FIELD = {
    'follow_identity_id': '',
    'follow_follower_id': ''
}