from .base import *
from .base import env

# ==============================================================================
# CONFIGURAÇÕES GERAIS DE PRODUÇÃO
# ==============================================================================
DEBUG = False
SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

# ==============================================================================
# CONFIGURAÇÕES DE SEGURANÇA (HTTPS)
# ==============================================================================
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000  # 1 ano
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ==============================================================================
# BANCO DE DADOS
# ==============================================================================
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# ==============================================================================
# CORS (Para permitir a comunicação com o frontend na Vercel)
# ==============================================================================
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")
CORS_ALLOW_CREDENTIALS = True


# ==============================================================================
# DJ-REST-AUTH & ALLAUTH
# ==============================================================================
# Garante que os cookies funcionem corretamente com HTTPS
REST_AUTH.update({
    "JWT_AUTH_SECURE": True,
    "JWT_AUTH_SAMESITE": "None",
})
SIMPLE_JWT.update({
    "COOKIE_SECURE": True,
    "COOKIE_SAMESITE": "None",
})

