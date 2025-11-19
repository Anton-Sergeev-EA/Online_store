from django.db import models
from django.conf import settings


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('confirmed', 'Подтвержден'),
        ('delivering', 'Доставляется'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='orders',
                             verbose_name='Пользователь')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
                              default='new', verbose_name='Статус')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                       verbose_name='Общая сумма')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Дата обновления')
    shipping_address = models.TextField(verbose_name='Адрес доставки')
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заказ #{self.id} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.shipping_address and hasattr(self.user, 'address'):
            self.shipping_address = self.user.address
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='items', verbose_name='Заказ')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE,
                                verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name='Цена на момент заказа')
    
    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def total_price(self):
        return self.price * self.quantity
    