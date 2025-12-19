from .base import *

DEBUG = True

# Используем SQLite для локальной разработки.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
