from .base import *
import os
import dj_database_url

DEBUG = False

# Настройки для Docker/Production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'online_store_db'),
        'USER': os.environ.get('DB_USER', 'store_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'store_password'),
        'HOST': os.environ.get('DB_HOST', 'db'),  # В Docker используем 'db'
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Или используем DATABASE_URL если она установлена
if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )

# Настройки безопасности для production
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
CSRF_TRUSTED_ORIGINS = ['https://your-domain.com', 'https://www.your-domain.com']

# HTTPS settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# HSTS settings
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
