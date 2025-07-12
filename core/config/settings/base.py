# HERE imports 

from datetime import timedelta
from pathlib import Path

import environ


# NOTE Should I remove cors in production ? 


env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ROOT_DIR = BASE_DIR / "core"


DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]


THIRD_PARTY_APPS = [
    "rest_framework",
    "django_filters",
    "corsheaders",
    "rest_framework.authtoken",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth",
    "dj_rest_auth.registration",
]

LOCAL_APPS = ["apps.common",  "apps.users", "apps.cache", "apps.agricultura", "apps.incite" ]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


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


ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"


# ── ⋙ ── ── ── ── ── ── ── ──➤
# _DB_ DATABASES
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'Incite',
        'USER': 'postgres',
        'PASSWORD': 'master',
        'HOST': 'localhost',
        'PORT': '5432',
    }
} 
# ── ⋙ ── ── ── ── ── ── ── ──➤


# DATABASES = {"default": env.db("DATABASE_URL")}
# DATABASES["default"]["ATOMIC_REQUESTS"] = True


PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]


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

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
SITE_ID = 1
ADMIN_URL = "lesecret/"


# _PIN_ : static and media files
#Change the static and media files place. 
#Located inside of the core folder 
STATIC_URL = "/staticfiles/"
STATIC_ROOT = str(ROOT_DIR / "staticfiles")
MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = str(ROOT_DIR / "mediafiles")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User" # ✳ AUTH_USER_MODEL

# WARN: AllowAny permission 
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        # "rest_framework.permissions.IsAuthenticated", 
        "rest_framework.permissions.AllowAny",
    ],
}


# ── ◯⫘⫘⫘⫘  dj-rest-auth  ⫘⫘⫘⫘⫘⫸


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(seconds=20),# _PIN_ ⏰ ACCESS_TOKEN_LIFETIME
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1), 
    "ROTATE_REFRESH_TOKENS": False,
    # "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "SIGNING_KEY": "Q_OlLlrzNWu4dvgRbyrv7g0PQ30txCl9dD7xounpZLB0rvdn0xc",  # [ENV]
    "COOKIE_NAME": "access-token",
    "COOKIE_SECURE": True,  # WARN pra funcionar em dev
    "COOKIE_HTTPONLY": True,
    "COOKIE_SAMESITE": "None",   # WARN pra funcionar em dev
}


REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "access-token",
    "JWT_AUTH_REFRESH_COOKIE": "refresh-token",
    'JWT_AUTH_SECURE': True, # _PIN_ Set to true in https
    'JWT_AUTH_HTTPONLY': True,
    'JWT_AUTH_SAMESITE': 'None', # Lax, Strict
    "REGISTER_SERIALIZER": "apps.users.serializers.CustomRegisterSerializer", # _PIN_ Overriding these Serializers
    "USER_DETAILS_SERIALIZER": "apps.users.serializers.UserSerializer",
}

# Configuração do Allauth (dj-rest-auth depende dele)
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
# ACCOUNT_CONFIRM_EMAIL_ON_GET = True
# ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False


AUTHENTICATION_BACKENDS = [
    "allauth.account.auth_backends.AuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
]


# ──  ⋙── ── ── LOGGING ── ── ── ──➤
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(name)-12s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}
