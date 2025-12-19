"""
Конфигурация WSGI для проекта online_store.
Он предоставляет вызываемый объект WSGI в виде переменной уровня модуля с
именем`application. Дополнительную информацию об этом файле см. в разделе
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_store.settings')

application = get_wsgi_application()
