import os
from pathlib import Path

import pymysql
from bkcrypto.constants import SymmetricCipherType
from environ import environ
from ovinc_client.core.logger import get_logging_config_dict
from ovinc_client.core.utils import getenv_or_raise, strtobool

pymysql.install_as_MySQLdb()

# Base Dir
BASE_DIR = Path(__file__).resolve().parent.parent

# Env
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# DEBUG
DEBUG = strtobool(os.getenv("DEBUG", "False"))

# APP_CODE & SECRET
APP_CODE = getenv_or_raise("APP_CODE")
APP_SECRET = getenv_or_raise("APP_SECRET")
SECRET_KEY = getenv_or_raise("APP_SECRET")

# Hosts
BACKEND_URL = getenv_or_raise("BACKEND_URL")
ALLOWED_HOSTS = getenv_or_raise("ALLOWED_HOSTS").split(",")
CORS_ALLOW_CREDENTIALS = strtobool(os.getenv("CORS_ALLOW_CREDENTIALS", "True"))
CORS_ORIGIN_WHITELIST = getenv_or_raise("CORS_ORIGIN_WHITELIST").split(",")
CSRF_TRUSTED_ORIGINS = CORS_ORIGIN_WHITELIST
FRONTEND_URL = getenv_or_raise("FRONTEND_URL")

# APPs
INSTALLED_APPS = [
    "daphne",
    "corsheaders",
    "simpleui",
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "adrf",
    "sslserver",
    "ovinc_client.account",
    "ovinc_client.trace",
    "apps.bk_crypto",
    "apps.cel",
    "apps.cos",
    "apps.doc",
    "apps.home",
    "apps.permission",
]

# MIDDLEWARE
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "ovinc_client.core.middlewares.CSRFExemptMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "ovinc_client.core.middlewares.OAuthMiddleware",
    "apps.home.middlewares.UserWhitelistMiddleware",
    "ovinc_client.core.middlewares.SQLDebugMiddleware",
]
if not DEBUG:
    MIDDLEWARE += ["ovinc_client.core.middlewares.UnHandleExceptionMiddleware"]

# Urls
ROOT_URLCONF = "entry.urls"

# TEMPLATES
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# DB and Cache
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": getenv_or_raise("DB_NAME"),
        "USER": getenv_or_raise("DB_USER"),
        "PASSWORD": getenv_or_raise("DB_PASSWORD"),
        "HOST": getenv_or_raise("DB_HOST"),
        "PORT": int(getenv_or_raise("DB_PORT")),
        "CONN_MAX_AGE": int(os.getenv("DB_CONN_MAX_AGE", str(60 * 60))),
        "OPTIONS": {"charset": "utf8mb4"},
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
REDIS_HOST = getenv_or_raise("REDIS_HOST")
REDIS_PORT = int(getenv_or_raise("REDIS_PORT"))
REDIS_PASSWORD = getenv_or_raise("REDIS_PASSWORD")
REDIS_DB = int(getenv_or_raise("REDIS_DB"))
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
    }
}

# ASGI
ASGI_APPLICATION = "entry.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
            ],
        },
    },
}

# Auth
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
AUTHENTICATION_BACKENDS = ["ovinc_client.core.auth.OAuthBackend"]
OVINC_TICKET_COOKIE_NAME = getenv_or_raise("OVINC_TICKET_COOKIE_NAME")

# International
LANGUAGE_CODE = os.getenv("DEFAULT_LANGUAGE", "zh-hans")
TIME_ZONE = os.getenv("DEFAULT_TIME_ZONE", "Asia/Shanghai")
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = (("zh-hans", "中文简体"), ("en", "English"))
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

# Static
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "staticfiles")]

# Session
SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", f"{'dev-' if DEBUG else ''}{APP_CODE}-sessionid")
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_AGE = int(os.getenv("SESSION_COOKIE_AGE", str(60 * 60 * 24 * 7)))
SESSION_COOKIE_DOMAIN = os.getenv("SESSION_COOKIE_DOMAIN")

# Log
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOGGING = get_logging_config_dict(LOG_LEVEL, LOG_DIR)

# rest_framework
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["ovinc_client.core.renderers.APIRenderer"],
    "DEFAULT_PAGINATION_CLASS": "ovinc_client.core.paginations.NumPagination",
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M%z",
    "DEFAULT_THROTTLE_RATES": {},
    "EXCEPTION_HANDLER": "ovinc_client.core.exceptions.exception_handler",
    "UNAUTHENTICATED_USER": "ovinc_client.account.models.CustomAnonymousUser",
    "DEFAULT_AUTHENTICATION_CLASSES": ["ovinc_client.core.auth.LoginRequiredAuthenticate"],
}

# User
AUTH_USER_MODEL = "account.User"

# Celery
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_ACCEPT_CONTENT = ["pickle", "json"]
BROKER_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

# APM
ENABLE_TRACE = strtobool(os.getenv("ENABLE_TRACE", "False"))
SERVICE_NAME = os.getenv("SERVICE_NAME", APP_CODE)
OTLP_HOST = os.getenv("OTLP_HOST", "http://127.0.0.1:4317")
OTLP_TOKEN = os.getenv("OTLP_TOKEN", "")

# RUM
RUM_ID = os.getenv("RUM_ID", "")
RUM_HOST = os.getenv("RUM_HOST", "https://rumt-zh.com")

# OVINC
OVINC_API_DOMAIN = getenv_or_raise("OVINC_API_DOMAIN")
OVINC_WEB_URL = getenv_or_raise("OVINC_WEB_URL")

# Crypto (using encryption may significantly impact server performance)
ENABLE_BKCRYPTO = strtobool(os.getenv("ENABLE_BKCRYPTO", "False"))
BKCRYPTO = {
    "SYMMETRIC_CIPHER_TYPE": SymmetricCipherType.SM4.value,
    "SYMMETRIC_CIPHERS": {"default": {"common": {"key": APP_SECRET}}},
}

# QCLOUD
QCLOUD_SECRET_ID = os.getenv("QCLOUD_SECRET_ID")
QCLOUD_SECRET_KEY = os.getenv("QCLOUD_SECRET_KEY")

# CDN
QCLOUD_CDN_SIGN_KEY_URL_PARAM = os.getenv("QCLOUD_CDN_SIGN_KEY_URL_PARAM", "sign")
QCLOUD_CDN_SIGN_KEY = os.getenv("QCLOUD_CDN_SIGN_KEY")

# COS
QCLOUD_COS_REGION = os.getenv("QCLOUD_COS_REGION", "ap-beijing")
QCLOUD_COS_BUCKET = os.getenv("QCLOUD_COS_BUCKET")
QCLOUD_COS_URL = os.getenv("QCLOUD_COS_URL")
QCLOUD_API_DOMAIN_TMPL = os.getenv("QCLOUD_API_DOMAIN_TMPL", "{}.tencentcloudapi.com")
QCLOUD_API_SCHEME = os.getenv("QCLOUD_API_SCHEME", "https")
QCLOUD_STS_EXPIRE_TIME = int(os.getenv("QCLOUD_STS_EXPIRE_TIME", str(60 * 10)))
QCLOUD_COS_IMAGE_FORMAT = os.getenv("QCLOUD_COS_IMAGE_FORMAT", "imageMogr2/quality/80/format/webp/interlace/1")
QCLOUD_COS_IMAGE_SUFFIX = ["jpg", "jpeg", "png", "bmp", "webp", "tiff", "gif", "avif", "heif", "heic", "tpg", "apng"]

# Captcha
CAPTCHA_TCLOUD_ID = os.getenv("CAPTCHA_TCLOUD_ID", QCLOUD_SECRET_ID)
CAPTCHA_TCLOUD_KEY = os.getenv("CAPTCHA_TCLOUD_KEY", QCLOUD_SECRET_KEY)
CAPTCHA_ENABLED = strtobool(os.getenv("CAPTCHA_ENABLED", "False"))
CAPTCHA_APP_ID = int(os.getenv("CAPTCHA_APP_ID", "0"))
CAPTCHA_APP_SECRET = os.getenv("CAPTCHA_APP_SECRET", "")
CAPTCHA_APP_INFO_TIMEOUT = int(os.getenv("CAPTCHA_APP_INFO_TIMEOUT", str(60 * 10)))

# User Whitelist
USER_WHITELIST = [u for u in os.getenv("USER_WHITELIST", "").split(",") if u]

# Doc
# One of DocSearchType
DOC_SEARCH_TYPE = os.getenv("DOC_SEARCH_TYPE", "all")
DOC_RSS_BUILD_SIZE = int(os.getenv("DOC_RSS_BUILD_SIZE", "100"))
DOC_RSS_BUILD_TITLE = os.getenv("DOC_RSS_BUILD_TITLE")
DOC_RSS_BUILD_DESCRIPTION = os.getenv("DOC_RSS_BUILD_DESCRIPTION")
DOC_RSS_BUILD_PATH = os.getenv("DOC_RSS_BUILD_PATH", "rss.xml")
