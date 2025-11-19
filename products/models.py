from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('products_by_category', args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name='Цена')
    image = models.ImageField(upload_to='products/', blank=True, null=True,
                              verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='products',
                                 verbose_name='Категория')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])
    
    def get_available_quantity(self):
        try:
            stock = self.stock
            return stock.quantity - stock.reserved
        except:
            return 0


class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE,
                                   related_name='stock', verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=0,
                                           verbose_name='Количество на складе')
    reserved = models.PositiveIntegerField(default=0,
                                           verbose_name='Зарезервировано')
    
    class Meta:
        verbose_name = 'Остаток'
        verbose_name_plural = 'Остатки'
    
    def __str__(self):
        return f"{self.product.name}: {self.available_quantity} доступно"
    
    @property
    def available_quantity(self):
        return self.quantity - self.reserved
    