import os
import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-@=34_6+7@__b9br5$*#*ywmlh*aco__-jg87!*8b53%m+veidy'

DEBUG = True

ALLOWED_HOSTS = [
    'probashiapi.algorithmgeneration.com',
	'192.168.0.101',
	'127.0.0.1'
    ]

# user model
AUTH_USER_MODEL = 'auth_user_app.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #created apps
    'auth_user_app',
    'user_profile_app',
    'consultancy_app',
    'user_setting_other_app',
    'user_connection_app',
    'user_blog_app',
    'user_chat_app',

    #third party apps
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'probashi_backend.urls'

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

WSGI_APPLICATION = 'probashi_backend.wsgi.application'


# CORS WHITELIST
#CORS_ORIGIN_WHITELIST = [
    #"http://127.0.0.1:8080"
#]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',
    'http://localhost:8080',
    'http://127.0.0.1:4200',
    'https://probashiapi.algorithmgeneration.com',
    'http://probashiapi.algorithmgeneration.com',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'X-Api-Key'
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'probashi_db',
        'USER': 'agl',
        'PASSWORD': '12345',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}



REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'NON_FIELD_ERRORS_KEY': 'error',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=100),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'USER_ID_FIELD': 'userid',
    # 'ROTATE_REFRESH_TOKENS': True,
    # 'BLACKLIST_AFTER_ROTATION': True
}





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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True



STATIC_URL = 'static/'

STATIC_ROOT= os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'probashi_backend/static')
]
MEDIA_URL = '/upload/'
MEDIA_ROOT=os.path.join(BASE_DIR, "upload")


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_PORT = '2525'
EMAIL_HOST_USER = '60974a6dc6308a'
EMAIL_HOST_PASSWORD = '85c90c396ab965'

