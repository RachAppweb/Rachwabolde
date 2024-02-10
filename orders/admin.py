from django.contrib import admin
from .models import *
# Register your models here.


class OrderProductInline(admin.TabularInline):
    model = OrderProduct

    readonly_fields = ['payment', 'user', 'quantity',
                       'product', 'product_price', 'ordered']
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'fullname', 'phone_number',
                    'order_total',  'is_ordered', 'created_at']
    list_filter = ['is_ordered']
    search_fields = ['phone_number', 'first_name', 'last_name', 'email']
    list_per_page = 15
    inlines = [OrderProductInline]


admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
