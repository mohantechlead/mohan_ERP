from django.contrib import admin
from .models import orders,delivery,orders_items

admin.site.register(orders)
admin.site.register(delivery)
admin.site.register(orders_items)
