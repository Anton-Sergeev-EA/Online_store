from .base import *

DEBUG = True

# Используем SQLite для локальной разработки
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Или если хотите использовать PostgreSQL локально, раскомментируйте:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'online_store_db',
#         'USER': 'store_user',
#         'PASSWORD': 'store_password',
#         'HOST': 'localhost',  # Используем localhost вместо db
#         'PORT': '5432',
#     }
# }