from django.contrib import admin
from .models import FGRN,FGRN_item, finished_goods,items_list

admin.site.register(FGRN)
admin.site.register(FGRN_item)
admin.site.register(finished_goods)
admin.site.register(items_list)
