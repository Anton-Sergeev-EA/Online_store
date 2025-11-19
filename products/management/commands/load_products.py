import json
import csv
from django.core.management.base import BaseCommand
from django.core.files import File
from products.models import Category, Product, Stock
import os


class Command(BaseCommand):
    help = 'Загрузка товаров из JSON или CSV файла'
    
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str,
                            help='Путь к файлу с данными')
        parser.add_argument('--format', type=str, default='json',
                            choices=['json', 'csv'], help='Формат файла')
    
    def handle(self, *args, **options):
        file_path = options['file_path']
        file_format = options['format']
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'Файл {file_path} не найден'))
            return
        
        try:
            if file_format == 'json':
                self.load_from_json(file_path)
            else:
                self.load_from_csv(file_path)
            
            self.stdout.write(self.style.SUCCESS('Товары успешно загружены'))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при загрузке: {str(e)}'))
    
    def load_from_json(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for item in data:
            self.create_product(item)
    
    def load_from_csv(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.create_product(row)
    
    def create_product(self, data):
        # Получаем или создаем категорию
        category, created = Category.objects.get_or_create(
            name=data['category'],
            defaults={
                'slug': data.get('category_slug', data['category'].lower())}
        )
        
        # Создаем товар
        product, created = Product.objects.get_or_create(
            name=data['name'],
            defaults={
                'slug': data.get('slug', data['name'].lower()),
                'description': data.get('description', ''),
                'price': data['price'],
                'category': category,
            }
        )
        
        # Создаем остатки
        stock, created = Stock.objects.get_or_create(
            product=product,
            defaults={
                'quantity': data.get('quantity', 0),
                'reserved': data.get('reserved', 0),
            }
        )
        