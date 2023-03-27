from django.contrib import admin

from .models import Orders

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'order_number',
        'price_usd',
        'price_rub',
        'shipping_date',
    )

    search_fields = ('order_number',)


admin.site.register(Orders, OrderAdmin)