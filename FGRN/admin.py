from django.contrib import admin
from .models import FGRN,FGRN_item, finished_goods,items_list, FGRNopening_balance, inventory_FGRN_items, FinishedGoodsGroup

admin.site.register(FGRN)
admin.site.register(FGRN_item)
admin.site.register(finished_goods)
admin.site.register(items_list)
admin.site.register(FGRNopening_balance)
admin.site.register(inventory_FGRN_items)
admin.site.register(FinishedGoodsGroup)


# @admin.register(FinishedGoodsGroup)
# class FinishedGoodsGroupAdmin(admin.ModelAdmin):
#     list_display = ('group_name', 'finished_good', 'created_at')
#     filter_horizontal = ('order_items',)

