from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    show_change_link = True
    verbose_name = 'Товар'
    verbose_name_plural = 'Список товаров'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'first_name',
        'last_name',
        'email',
        'country',
        'address',
        'postal_code',
        'city',
        'created',
        'get_order_price',
        'paid',
    ]
    search_fields = ['id', 'user__username']
    list_editable = ['paid']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

    def get_order_price(self, obj):
        return obj.order_price
    get_order_price.__name__ = 'Сумма'
