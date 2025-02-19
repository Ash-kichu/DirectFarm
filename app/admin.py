from django.contrib import admin
from .models import Product, Cart, CartItem, Order, OrderItem, User

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'availability', 'farmer', 'created_at')
    list_filter = ('category', 'availability')
    search_fields = ('name', 'farmer')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'created_at')
    list_filter = ('cart', 'product')
    search_fields = ('cart__user__username', 'product__name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'payment_method','created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'status')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'created_at')
    list_filter = ('order', 'product')
    search_fields = ('order__user__username', 'product__name')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'gender', 'phone', 'location', 'joined_at')
    list_filter = ('user_type', 'gender', 'joined_at')
    search_fields = ('username', 'email', 'phone')
