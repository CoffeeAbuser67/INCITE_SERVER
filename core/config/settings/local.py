
# HERE 
from .base import *
from .base import env

SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = True

DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

SIMPLE_JWT.update({
    "COOKIE_SECURE": True,
    "COOKIE_SAMESITE": "None",
})

REST_AUTH.update({
    "JWT_AUTH_SECURE": True,
    "JWT_AUTH_SAMESITE": "None",
})

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True

ALLOWED_HOSTS = ["*"]

