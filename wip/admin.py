from django.contrib import admin

from .models import WIP, WIP_item


class WIP_itemInline(admin.TabularInline):
    model = WIP_item
    extra = 0


@admin.register(WIP)
class WIPAdmin(admin.ModelAdmin):
    list_display = ('WIP_no', 'date', 'work_center', 'branch')
    inlines = [WIP_itemInline]


@admin.register(WIP_item)
class WIP_itemAdmin(admin.ModelAdmin):
    list_display = (
        'WIP_no',
        'item_name',
        'quantity',
        'no_of_unit',
        'unit_type',
        'per_unit_kg',
        'measurement_type',
    )
