import os
import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-@=34_6+7@__b9br5$*#*ywmlh*aco__-jg87!*8b53%m+veidy"

DEBUG = True

ALLOWED_HOSTS = [
    "probashiapi.algorithmgeneration.com",
    "192.168.0.101",
    "127.0.0.1",
    "192.168.100.87",
    "114.129.10.3",
    "192.168.50.87",
]

# user model
AUTH_USER_MODEL = "auth_user_app.User"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "auth_user_app.customAuth.CustomerBackendForPhoneNumber",
]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party apps
    "channels",
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt.token_blacklist",
    "import_export",
    # created apps
    "auth_user_app",
    "user_profile_app",
    "consultancy_app",
    "user_setting_other_app",
    "user_connection_app",
    "user_blog_app",
    "user_chat_app",
    "social_auth",

    "django_extensions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "probashi_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
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

# WSGI_APPLICATION = 'probashi_backend.wsgi.application'
ASGI_APPLICATION = "probashi_backend.asgi.application"


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}


# CORS WHITELIST
# CORS_ORIGIN_WHITELIST = [
# "http://127.0.0.1:8080"
# ]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "http://localhost:8080",
    "http://127.0.0.1:4200",
    "https://probashiapi.algorithmgeneration.com",
    "http://probashiapi.algorithmgeneration.com",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "X-Api-Key",
]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "probashi_db",
        "USER": "agl",
        "PASSWORD": "12345",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    },
    "probashi_chat": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "probashichat_db",
        "USER": "agl",
        "PASSWORD": "12345",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    },
}

DATABASE_ROUTERS = [
    "db_routers.db_routers.ChatRouter",
]


REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10,
    "NON_FIELD_ERRORS_KEY": "error",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # 'EXCEPTION_HANDLER': 'probashi_backend.custom_exception_handler.custom_exception_handler',
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(days=30, minutes=100),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=90),
    "USER_ID_FIELD": "userid",
    # 'ROTATE_REFRESH_TOKENS': True,
    # 'BLACKLIST_AFTER_ROTATION': True
}


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


LANGUAGE_CODE = "en-us"

# TIME_ZONE = "Asia/Dhaka"
TIME_ZONE = "UTC"
USE_I18N = True

# USE_L10N = False

USE_TZ = True


image_directory = Path(__file__).resolve().parent.parent.parent.parent

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'probashi_backend/static')
]
MEDIA_URL = "/probashi_images/"
MEDIA_ROOT = os.path.join(image_directory, "probashi_images")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.mailtrap.io'
# EMAIL_PORT = '2525'
# EMAIL_HOST_USER = '60974a6dc6308a'
# EMAIL_HOST_PASSWORD = '85c90c396ab965'

EMAIL_USE_TLS = True
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "agtests@adnanfoundation.com"
EMAIL_HOST_PASSWORD = "@adnanfoundation"


# import xlxs to table data
# IMPORT_EXPORT_IMPORT_PERMISSION_CODE = 'delete'
# IMPORT_EXPORT_EXPORT_PERMISSION_CODE = 'delete'
# IMPORT_EXPORT_USE_TRANSACTIONS = True
