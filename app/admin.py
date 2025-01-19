from django.contrib import admin
from .models import Product, Farmer

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'availability', 'farmer', 'created_at')
    list_filter = ('category', 'availability')
    search_fields = ('name', 'farmer')

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'farm_name', 'joined_at')
    list_filter = ('location', 'joined_at', 'gender')
    search_fields = ('user', 'farm_name', 'location')
