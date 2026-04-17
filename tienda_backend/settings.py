import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# SEGURIDAD
# =========================
SECRET_KEY = os.environ.get("SECRET_KEY", "inseguro-dev")
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "ecommerce-django-e44l.onrender.com",
    "ecommerce-jorge-patricio.vercel.app",
]

# =========================
# APPS
# =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',

    'rest_framework',
    'django_filters',
    'corsheaders',

    # Google login
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # Auth REST
    'dj_rest_auth',
    'dj_rest_auth.registration',

    'tienda',
]

SITE_ID = 1

# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    # 🔥 necesario para allauth
    'allauth.account.middleware.AccountMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =========================
# AUTH BACKENDS
# =========================
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# =========================
# ALLAUTH CONFIG
# =========================
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
LOGIN_REDIRECT_URL = '/'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}

# =========================
# EMAIL
# =========================
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# =========================
# DJ REST AUTH (FIX TOKEN)
# =========================
REST_AUTH = {
    'TOKEN_MODEL': None
}

# =========================
# URLS
# =========================
ROOT_URLCONF = 'tienda_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',  # 🔥 FIX FINAL
            ],
        },
    },
]

WSGI_APPLICATION = 'tienda_backend.wsgi.application'

# =========================
# DATABASE
# =========================
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True
    )
}

# =========================
# REST + JWT
# =========================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=48),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

REST_USE_JWT = True

# =========================
# STATIC
# =========================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# =========================
# CORS
# =========================
CORS_ALLOWED_ORIGINS = [
    "https://ecommerce-jorge-patricio.vercel.app",
]

# =========================
# SECURITY
# =========================
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
