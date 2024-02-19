"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta
import boto3
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-m+!_#j9t!jp%v3g(k*##ws0j97h=ub+978f4kcta9of5gregni'

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = []
IS_LOCAL_DEV = str(os.environ.get('IS_LOCAL_DEV')) in ("true")
DEBUG = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    # 3rd party
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
    'fullurl',
    # 'django_extensions',
    'crispy_forms',
    'shortener',
    'firebase_admin',
    'celery',
    'django_celery_beat',

    # allauth
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.sites',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'rest_framework.authtoken',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # allauth providers
    # 'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.apple',
    'allauth.socialaccount.providers.google',

    # own apps
    'users',
    'user_info',

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # `allauth` needs this from django
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

}


# JWT Token config
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=90),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=120)
}

# Django rest-auth config telling to use JWT config
REST_USE_JWT = True

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static-files') if DEBUG else '/static-files/'
STATIC_URL = '/static-files/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media-files') if DEBUG else '/media-files/'
MEDIA_URL = '/media-files/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SITE_ID = 1


if 'EKS' in os.environ:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']
    EMAIL_USE_TLS = os.environ['EMAIL_USE_TLS']
    EMAIL_HOST = os.environ['EMAIL_HOST']
    EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
    EMAIL_PORT = os.environ['EMAIL_PORT']
else:
    # Use Gmail as the email backend
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    # The email address to use for various automated correspondence from the site manager(s).
    DEFAULT_FROM_EMAIL = 'djangosaynode@gmail.com'

    # Use TLS when connecting to Gmail's SMTP server (TLS is required for Gmail)
    EMAIL_USE_TLS = True

    # Gmail SMTP server address
    EMAIL_HOST = 'smtp.gmail.com'

    # Your Gmail username (full email address)
    EMAIL_HOST_USER = 'djangosaynode@gmail.com'

    # Your Gmail password (You may want to use an 'App Password' generated in your Google Account)
    EMAIL_HOST_PASSWORD = 'ethg uhbx mqbn kglx'

    # Gmail SMTP server port (587 is the default port for TLS)
    EMAIL_PORT = 587

OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_EMAIL_REQUIRED = True

# Makes sure User can log in even if not verified, other options are "mandatory" and then login is blocked until
# verified To edit the redirect page when User clicks the link to verify go to => templates=>account=>
# email_confirm.html To edit the email template go to => templates => account => email =>
# email_confirmation_message.txt / email_confirmation_subject.txt

ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_AUTHENTICATION_METHOD = 'email_username'
ACCOUNT_MAX_EMAIL_ADDRESSES = 1
# verify the email address once clicked on link sent to User email
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
# redirect to the auth library verify URL
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = ''
# subject prefix for verification email
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[ChainStaff.io]"
# redirect to the auth library verify URL
EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = ''

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 30
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None

REST_AUTH_SERIALIZERS = {
    'PASSWORD_RESET_SERIALIZER': 'password_reset.serializers.CustomPasswordResetSerializer'
}

# Custom User model needed or cannot register user
AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

