from django.contrib import admin
from .models import FGRN,FGRN_item, finished_goods

admin.site.register(FGRN)
admin.site.register(FGRN_item)
admin.site.register(finished_goods)
