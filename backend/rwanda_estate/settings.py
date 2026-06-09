# import os
# from pathlib import Path
# import environ

# env = environ.Env()
# environ.Env.read_env()

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent


# # Quick-start development settings - unsuitable for production
# # See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = env('SECRET_KEY', default='django-insecure-change-me')
# DEBUG = env.bool('DEBUG', default=True)
# ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1', '10.0.2.2'])
# # SECURITY WARNING: don't run with debug turned on in production!


# Application definition

# INSTALLED_APPS = [
#     'daphne',
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'rest_framework',
#     'rest_framework_simplejwt',
#     'rest_framework_simplejwt.token_blacklist',
#     'corsheaders',
#     'django_filters',
#     'phonenumber_field',
#     'drf_spectacular',
#     'accounts',
#     'listings',
#     'agents',
#     'messaging',
#     'payments',
#     'notifications',
#     'search',
# ]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'corsheaders.middleware.CorsMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'rwanda_estate.urls'
# TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 
#               'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True, 'OPTIONS': 
#               {'context_processors': ['django.template.context_processors.debug', 
#                                       'django.template.context_processors.request', 
#                                       'django.contrib.auth.context_processors.auth', 
#                                       'django.contrib.messages.context_processors.messages']}}]

# WSGI_APPLICATION = 'rwanda_estate.wsgi.application'
# ASGI_APPLICATION = 'rwanda_estate.asgi.application'


# # Database
# # https://docs.djangoproject.com/en/6.0/ref/settings/#databases

# USE_SQLITE = env.bool('USE_SQLITE', default=True)
# if USE_SQLITE:
#     DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
# else:
#     DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': env('DB_NAME', 'rwanda_estate'), 'USER': env('DB_USER', 'postgres'), 'PASSWORD': env('DB_PASSWORD', 'postgres'), 'HOST': env('DB_HOST', 'localhost'), 'PORT': env('DB_PORT', '5432')}}




# # Password validation
# # https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

# AUTH_USER_MODEL = 'accounts.User'
# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},    
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]


# # Internationalization
# # https://docs.djangoproject.com/en/6.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'Africa/Kigali'

# USE_I18N = True

# USE_TZ = True


# # Static files (CSS, JavaScript, Images)
# # https://docs.djangoproject.com/en/6.0/howto/static-files/

# STATIC_URL = 'static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles'
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication'],
#     'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
#     'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend', 'rest_framework.filters.SearchFilter', 'rest_framework.filters.OrderingFilter'],
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': 20,
#     'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
# }

# from datetime import timedelta
# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
#     'ROTATE_REFRESH_TOKENS': True,
#     'BLACKLIST_AFTER_ROTATION': True,
# }

# CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=['http://localhost:3000', 'http://localhost:8081'])
# CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://localhost:6379/0')
# CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default='redis://localhost:6379/1')
# CHANNEL_LAYERS = {'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'}}
# PHONENUMBER_DEFAULT_REGION = 'RW'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# ELASTICSEARCH_DSL = {'default': {'hosts': env('ELASTICSEARCH_HOST', default='localhost:9200')}}
#===========================================================================================================================================================

import os
from pathlib import Path
from datetime import timedelta
import environ

# -----------------------------------------------------------------------------
# ENVIRONMENT
# -----------------------------------------------------------------------------

env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------------------------------------------------
# SECURITY
# -----------------------------------------------------------------------------

SECRET_KEY = env(
    'SECRET_KEY',
    default='django-insecure-change-me-in-production'
)

DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = env.list(
    'ALLOWED_HOSTS',
    default=['localhost', '127.0.0.1', '10.0.2.2']
)

# -----------------------------------------------------------------------------
# APPLICATIONS
# -----------------------------------------------------------------------------

INSTALLED_APPS = [
    # ASGI
    'daphne',

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_filters',
    'phonenumber_field',
    'drf_spectacular',
    'storages',

    # Local apps
    'accounts',
    'listings',
    'agents',
    'messaging',
    'payments',
    'notifications',
    'search',
]

# -----------------------------------------------------------------------------
# MIDDLEWARE
# -----------------------------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -----------------------------------------------------------------------------
# URLS / TEMPLATES
# -----------------------------------------------------------------------------

ROOT_URLCONF = 'rwanda_estate.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'rwanda_estate.wsgi.application'
ASGI_APPLICATION = 'rwanda_estate.asgi.application'

# -----------------------------------------------------------------------------
# DATABASE
# -----------------------------------------------------------------------------

USE_SQLITE = env.bool('USE_SQLITE', default=True)

if USE_SQLITE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('DB_NAME', default='rwanda_estate'),
            'USER': env('DB_USER', default='postgres'),
            'PASSWORD': env('DB_PASSWORD', default='postgres'),
            'HOST': env('DB_HOST', default='localhost'),
            'PORT': env('DB_PORT', default='5432'),
        }
    }

# -----------------------------------------------------------------------------
# AUTHENTICATION
# -----------------------------------------------------------------------------

AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'
    },
]

# -----------------------------------------------------------------------------
# INTERNATIONALIZATION
# -----------------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Kigali'

USE_I18N = True
USE_TZ = True

# -----------------------------------------------------------------------------
# STATIC & MEDIA
# -----------------------------------------------------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------------------------------------------------------------
# DJANGO REST FRAMEWORK
# -----------------------------------------------------------------------------

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS':
        'drf_spectacular.openapi.AutoSchema',
}

# -----------------------------------------------------------------------------
# JWT
# -----------------------------------------------------------------------------

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# -----------------------------------------------------------------------------
# CORS
# -----------------------------------------------------------------------------

CORS_ALLOWED_ORIGINS = env.list(
    'CORS_ALLOWED_ORIGINS',
    default=[
        'http://localhost:3000',
        'http://localhost:8081',
    ]
)

# -----------------------------------------------------------------------------
# CELERY
# -----------------------------------------------------------------------------

CELERY_BROKER_URL = env(
    'CELERY_BROKER_URL',
    default='redis://localhost:6379/0'
)

CELERY_RESULT_BACKEND = env(
    'CELERY_RESULT_BACKEND',
    default='redis://localhost:6379/1'
)

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# -----------------------------------------------------------------------------
# CHANNELS
# -----------------------------------------------------------------------------

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [
                (
                    env('REDIS_HOST', default='localhost'),
                    env.int('REDIS_PORT', default=6379),
                )
            ],
        },
    },
}

# -----------------------------------------------------------------------------
# PHONE NUMBERS
# -----------------------------------------------------------------------------

PHONENUMBER_DEFAULT_REGION = 'RW'

# -----------------------------------------------------------------------------
# MTN MOMO
# -----------------------------------------------------------------------------

MTN_MOMO_API_KEY = env('MTN_MOMO_API_KEY', default='')
MTN_MOMO_SECRET_KEY = env('MTN_MOMO_SECRET_KEY', default='')
MTN_MOMO_ENVIRONMENT = env(
    'MTN_MOMO_ENVIRONMENT',
    default='sandbox'
)

# -----------------------------------------------------------------------------
# AIRTEL MONEY
# -----------------------------------------------------------------------------

AIRTEL_MONEY_API_KEY = env('AIRTEL_MONEY_API_KEY', default='')
AIRTEL_MONEY_SECRET_KEY = env('AIRTEL_MONEY_SECRET_KEY', default='')

# -----------------------------------------------------------------------------
# EMAIL
# -----------------------------------------------------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)

EMAIL_USE_TLS = True

EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')

# -----------------------------------------------------------------------------
# ELASTICSEARCH
# -----------------------------------------------------------------------------

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': env(
            'ELASTICSEARCH_HOST',
            default='localhost:9200'
        )
    }
}