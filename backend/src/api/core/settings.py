import os
from os.path import abspath, dirname, exists, join

import environ
from corsheaders.defaults import default_headers

# Load operating system env variables and prepare to use them
env = environ.Env()

# .env file, should load only in development environment
env_file = join(dirname(__file__), "local.env")
if exists(env_file):
    environ.Env.read_env(str(env_file))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = dirname(dirname(abspath(__file__)))

# Quick-start development settings - unsuitable for production
SECRET_KEY = env(
    "DJANGO_SECRET_KEY", default="8#ubdv*jh_1u(6m4)^s^*pdo!&y_#jz)vv%5cp%8^*&%ztttxq"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", False)
ENVIRONMENT = env("ENV")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=[])

# AWS
AWS_ACCESS_KEY = env.str("AWS_ACCESS_KEY", default="")
AWS_SECRET_KEY = env.str("AWS_SECRET_KEY", default="")
AWS_REGION = env.str("AWS_REGION", default="")

# CORS
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=False)
if not CORS_ALLOW_ALL_ORIGINS:
    CORS_ALLOWED_ORIGINS = env.str(
        "CORS_ALLOWED_ORIGINS", default="localhost,127.0.0.1"
    ).split(",")

CORS_ALLOW_HEADERS = list(default_headers) + ["network"]


# Application definition
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "django_extensions",
]

PROJECT_APPS = ["api.core", "api.exchange"]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "api.core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "api.core.wsgi.application"

# Django debug toolbar settings

if ENVIRONMENT == "development":
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INTERNAL_IPS = env.list("INTERNAL_IPS", default=[])
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda request: request.headers.get("x-requested-with")
        != "XMLHttpRequest"
    }

# Database

DATABASES = {
    "default": {
        "ENGINE": "",
        "NAME": "",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"}
]

# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = []

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

SITE_ID = 1

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files (uploads)

if ENVIRONMENT in ("development", "testing"):
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    MEDIA_ROOT = "uploads/"
    MEDIA_URL = "/uploads/"

# Email settings

if ENVIRONMENT in ("development", "testing"):
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = "no-reply@localhost"

# Django Rest Framework Settings

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "UNAUTHENTICATED_USER": None,
}


# Sentry
SENTRY_DSN = env.str("SENTRY_DSN", default=None)
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=ENVIRONMENT,
        integrations=[DjangoIntegration()],
    )

SPECTACULAR_SETTINGS = {
    "TITLE": "Token Factory",
    "VERSION": "1.0.0",
    "DESCRIPTION": "API Documentation",
}

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {
        "main_formatter": {
            "format": "%(levelname)s:%(name)s: %(message)s "
            "(%(asctime)s; %(filename)s:%(lineno)d)",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "main_formatter",
        },
    },
    "loggers": {
        "root": {
            "level": "INFO",
            "handlers": ["console"],
        },
    },
}

# CloudWatch Logging settings
AWS_CLOUDWATCH_LOG_GROUP_NAME = env.str("AWS_CLOUDWATCH_LOG_GROUP_NAME", default="")
if AWS_CLOUDWATCH_LOG_GROUP_NAME:
    import boto3

    boto3_logs_client = boto3.client(
        "logs",
        region_name=AWS_REGION,
    )
    LOGGING["handlers"]["cloudwatch"] = {
        "boto3_client": boto3_logs_client,
        "class": "logging.handlers.CloudWatchLogHandler",
        "level": "INFO",
        "filters": ["require_debug_false"],
        "formatter": "main_formatter",
        "log_group": AWS_CLOUDWATCH_LOG_GROUP_NAME,
        "stream_name": "cloudwatch",
    }
    LOGGING["loggers"]["root"]["handlers"].append("cloudwatch")


# Messenger

DEFAULT_MESSENGER = "EMAIL"


# Stellar

HORIZON_PUBLIC_API_SERVER = env.str(
    "HORIZON_PUBLIC_API_SERVER", default="https://horizon.stellar.org"
)
HORIZON_TEST_API_SERVER = env.str(
    "HORIZON_TEST_API_SERVER", default="https://horizon-testnet.stellar.org"
)
PUBLIC_NETWORK_PASSPHRASE = env.str(
    "PUBLIC_NETWORK_PASSPHRASE",
    default="Public Global Stellar Network ; September 2015",
)
TEST_NETWORK_PASSPHRASE = env.str(
    "TEST_NETWORK_PASSPHRASE", default="Test SDF Network ; September 2015"
)
TRANSACTION_TIMEOUT = env.int("TRANSACTION_TIMEOUT", default=1800)
ACCOUNT_STARTING_BALANCE = env.str("ACCOUNT_STARTING_BALANCE", default="2.01")
STELLAR_TOML_VERSION = env.str("STELLAR_TOML_VERSION", default="2.5.0")
DEFAULT_THRESHOLD = env.int("DEFAULT_THRESHOLD", default=21)
DEFAULT_SIGNER_LOW_WEIGHT = env.int("DEFAULT_SIGNER_LOW_WEIGHT", default=1)

# Credit Agricole Demo
EUR_CODE = "EUR"
EUR_ISSUER = "GBYSFWWH54OR6UP6EZIPG62Z4X6LPAKWFLKV7PZ5LDFFJC3UTTLIWJBA"
USD_CODE = "USD"
USD_ISSUER = "GD3S3NMR3FKIY4LUW6DBDJQE5AFKFBFLVDVAL4KWVHYMAN5ESSC4BKUD"
MAIN_WALLET_PK = "GA4EZFIF77K2DNNXWVU3W7A5ZQI7IEJBIAZSY7JNVZY5GVVOOIBTGVWT"
MAIN_WALLET_SK = "SA6GUC4UQ767MXTMMDEDWGNCBW2E6M56ZAGVJY2R4TOPYP2UXHHBXOLM"
PAYEES_LIST = ["GBHRMQS2Z6EKAR5Y6UU4ESFMRLU7ATX4WPUXL5FE4LCCU33EQQSFSASK","GDABK5INGNIER5O2Q7VZLRDUZFXYJ7E7ZQPDNQGQBWDYGLH6MTHWE2B5","GA5IIP4IG3EUML6MFZQNKC76XFQ6YXNORMHK6LGJPULMZAL5DAE7ZDEV","GD5JIWQLMX7Q4JRSKNNEJHPMBPO7VGUNJ2OAYGERFF5PNT4ULXINJDTK","GANMYE4PEQ3VFF7KYUE7NF5BQ2LXZ7IN2T3ZD42ISLKRZPBIS67KC23L","GD3MDSJBP2X5IV5XO2HYEJAZS43FWPCE75LLBZWJOMHMASQGNNYN7B7X"]
EUR_PRICE = env.float("EUR_PRICE", default=0.90909091)
USD_PRICE = env.float("USD_PRICE", default=1.10)
USERS = {
    "john": ("SDUEPWNZXG5NZ56YTDY2VT43OHNYC4HWBZMXDGGN75VSVXVCBLBG6H3M", 2),
    "jane": ("SA2PHAUK3WMCNMYXIO3A3HHOU5QJXVJPUE54N76WZTRKQ23XNDOEPLIP", 1),
    "amy": ("SBF74RX6W2FAWUZ5DLWD2FRIRW3SLR6CW4GOCMRZNQ4ZBFZDZ6VJYFSV", 1),
}
