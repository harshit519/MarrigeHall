from django.contrib import admin
from .models import Category, MenuItem, Order, OrderItem, Table

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'food_type', 'is_available', 'is_popular']
    list_filter = ['category', 'food_type', 'is_available', 'is_popular', 'is_spicy']
    search_fields = ['name', 'description']
    list_editable = ['is_available', 'is_popular']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'total_amount', 'delivery_type', 'status', 'created_at']
    list_filter = ['status', 'delivery_type', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['table_number', 'capacity', 'location', 'is_available']
    list_filter = ['is_available', 'location']
    search_fields = ['table_number']
