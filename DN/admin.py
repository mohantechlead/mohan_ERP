from django.contrib import admin
from .models import orders,delivery,orders_items,delivery_items, inventory_DN_items

admin.site.register(orders)
admin.site.register(delivery)
admin.site.register(delivery_items)
admin.site.register(orders_items)
admin.site.register(inventory_DN_items)
