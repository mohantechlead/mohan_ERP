from django.contrib import admin
from .models import purchase_orders,PR_item, GRN, GRN_item, HS_code,inventory_GRN_items

admin.site.register(GRN)
admin.site.register(GRN_item)
admin.site.register(HS_code)
admin.site.register(inventory_GRN_items)