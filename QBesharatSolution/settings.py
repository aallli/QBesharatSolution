"""
Django settings for QBesharatSolution project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _

VERSION = '0.18.1'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", default="az^xo9e_mq0xw#f@x%tvt)bi!o54f(^%%-@%1el@wpz53iie84")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DEBUG", default=1))

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", default="localhost").split(" ")

# Application definition

INSTALLED_APPS = [
    # third party apps
    'admin_interface',

    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party apps
    'colorfield',
    'jalali_date',
    'django_resized',
    'django_summernote',

    # my apps
    'QBesharat.apps.QBesharatConfig',
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
]

ROOT_URLCONF = 'QBesharatSolution.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'QBesharatSolution.wsgi.application'

AUTH_USER_MODEL = 'QBesharat.User'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ.get('DATABASES_HOST', default='127.0.0.1'),
        'PORT': os.environ.get('DATABASES_PORT', default='5432'),
        'NAME': os.environ.get('DATABASES_NAME', default='qbesharat'),
        'USER': os.environ.get('DATABASES_USER', default='postgres'),
        'PASSWORD': os.environ.get('DATABASES_PASSWORD', default='123'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = 'fa'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = False

LANGUAGES = [
    ('en', _('En')),
    ('fa', _('Fa')),
]

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'QBesharatSolution/static'),
    MEDIA_ROOT,
    TEMPLATES[0]['DIRS'][0],
]

# Image sizes
MAX_SMALL_IMAGE_WIDTH = 150  # in pixel
MAX_SMALL_IMAGE_HEIGHT = 150  # in pixel
MAX_MEDIUM_IMAGE_WIDTH = 500  # in pixel
MAX_MEDIUM_IMAGE_HEIGHT = 500  # in pixel
MAX_LARGE_IMAGE_WIDTH = 1000  # in pixel
MAX_LARGE_IMAGE_HEIGHT = 1000  # in pixel

# Django-Resized image resizing tool
DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg", 'JPEG': ".jpeg", 'GIF': ".gif", 'PNG': ".png"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True

# Summernote richtext box
X_FRAME_OPTIONS = 'SAMEORIGIN'

SUMMERNOTE_CONFIG = {
    'summernote': {
        # Change editor size
        'width': '100%',

        # Or, set editor language/locale forcely
        'lang': 'fa-IR',
    },
    'toolbar': [
        ['style', ['bold', 'italic', 'underline', 'clear']],
        ['font', ['strikethrough', 'superscript', 'subscript']],
        ['fontsize', ['fontsize']],
        ['color', ['color']],
        ['para', ['ul', 'ol', 'paragraph']],
        ['height', ['height']],
        ['insert', ['table', 'link', 'hr']],
        ['misc', ['fullscreen', 'codeview', 'undo', 'redo']],
    ],
}

# django jalali datae defaults
JALALI_DATE_DEFAULTS = {
    'Strftime': {
        'date': '%y/%m/%d',
        'datetime': '%H:%M:%S _ %y/%m/%d',
    },
    'Static': {
        'js': [
            # loading datepicker
            'admin/js/django_jalali.min.js',
            # OR
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.core.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/calendar.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc-fa.js',
            # 'admin/js/main.js',
        ],
        'css': {
            'all': [
                'admin/jquery.ui.datepicker.jalali/themes/base/jquery-ui.min.css',
            ]
        }
    },
}

# admin info
ADMIN_TEL = os.environ.get('ADMIN_TEL', default='+98 21 2915 5120')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', default='qbesharat@irib.ir')

LIST_PER_PAGE = int(os.environ.get('LIST_PER_PAGE', default=50))

# Chat server configurations
CHAT_SERVER_URL = os.environ.get("CHAT_SERVER_URL", default='http://localhost:8888/')
CHAT_SERVER_TOKEN = os.environ.get("CHAT_SERVER_TOKEN", default='706ee0d7f416d94d64fc0a042f40cbb14bfe4718')
CHAT_SUPPORT_GROUP = os.environ.get("CHAT_SUPPORT_GROUP", default='Online Support')
CHAT_SUPPORT_REFRESH_INTERVAL = os.environ.get("CHAT_SUPPORT_REFRESH_INTERVAL", default=60)
ONLINE_SUPPORT = None