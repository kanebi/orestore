from django.contrib import admin
from .models import MenuItem, OrderItem, Order

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available', 'order', 'date_created', 'date_updated')
    list_filter = ('category', 'available', 'date_created', 'date_updated')
    search_fields = ('name', 'description', 'tags')
    ordering = ('order',)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'quantity', 'date_created', 'date_updated')
    list_filter = ('date_created', 'date_updated')
    search_fields = ('menu_item__name',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'status', 'payment_method', 'shipping_address', 'date_created', 'date_updated')
    list_filter = ('status', 'payment_method', 'date_created', 'date_updated')
    search_fields = ('customer__username', 'shipping_address')
    filter_horizontal = ('items',)

admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
