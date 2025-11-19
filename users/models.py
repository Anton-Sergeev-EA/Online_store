from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True,
                             verbose_name='Телефон')
    address = models.TextField(blank=True, null=True, verbose_name='Адрес')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата регистрации')
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f"{self.username} ({self.email})"
    