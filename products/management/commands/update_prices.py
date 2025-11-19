import csv
from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = 'Обновление цен товаров из CSV файла'
    
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str,
                            help='Путь к CSV файлу с ценами')
    
    def handle(self, *args, **options):
        file_path = options['file_path']
        
        updated_count = 0
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    product = Product.objects.get(name=row['name'])
                    old_price = product.price
                    product.price = row['price']
                    product.save()
                    updated_count += 1
                    self.stdout.write(
                        f'Обновлен {product.name}: {old_price} -> {product.price}')
                except Product.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'Товар {row["name"]} не найден'))
                except KeyError:
                    self.stdout.write(
                        self.style.ERROR('Некорректный формат CSV файла'))
                    break
        
        self.stdout.write(
            self.style.SUCCESS(f'Обновлено {updated_count} товаров'))
        