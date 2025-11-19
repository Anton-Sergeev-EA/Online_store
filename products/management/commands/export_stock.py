import csv
from django.core.management.base import BaseCommand
from products.models import Stock


class Command(BaseCommand):
    help = 'Экспорт остатков товаров в CSV файл'
    
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str,
                            help='Путь для сохранения CSV файла')
    
    def handle(self, *args, **options):
        file_path = options['file_path']
        
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(
                ['Товар', 'Категория', 'Цена', 'На складе', 'Зарезервировано',
                 'Доступно'])
            
            for stock in Stock.objects.select_related(
                    'product__category').all():
                writer.writerow([
                    stock.product.name,
                    stock.product.category.name,
                    stock.product.price,
                    stock.quantity,
                    stock.reserved,
                    stock.available_quantity,
                ])
        
        self.stdout.write(
            self.style.SUCCESS(f'Остатки экспортированы в {file_path}'))
        