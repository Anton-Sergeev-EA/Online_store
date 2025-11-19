import time
import os
import psycopg2
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Wait for database to be ready'
    
    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None
        for i in range(30):
            try:
                conn = psycopg2.connect(
                    host=os.environ.get('DB_HOST', 'db'),
                    database=os.environ.get('DB_NAME', 'online_store_db'),
                    user=os.environ.get('DB_USER', 'store_user'),
                    password=os.environ.get('DB_PASSWORD', 'store_password'),
                    port=os.environ.get('DB_PORT', '5432')
                )
                conn.close()
                self.stdout.write(self.style.SUCCESS('Database is ready!'))
                return
            except psycopg2.OperationalError:
                self.stdout.write(
                    f'Attempt {i + 1}/30: Database not ready, waiting 1 second...')
                time.sleep(1)
        
        self.stdout.write(
            self.style.ERROR('Database connection failed after 30 attempts'))
        exit(1)
        