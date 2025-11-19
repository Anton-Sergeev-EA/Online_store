from django.contrib import admin
from .models import Category, Product, Stock

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'description')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'reserved', 'available_quantity')
    search_fields = ('product__name',)
    