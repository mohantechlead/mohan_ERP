from django.contrib import admin
from django.urls import path, include
from FGRN import views
from FGRN import line_portal_views

urlpatterns = [
    path('create_fgrn', views.create_fgrn, name='create_fgrn'),
    path('display_goods', views.display_goods, name='display_goods'),
    path('display_FGRN', views.display_FGRN, name='display_fgrn'),
    path('fgrn_opening_balance', views.fgrn_opening_balances, name='fgrn_opening_balance'),
    path('display_single_fgrn/<str:FGRN_no>', views.display_single_fgrn, name='display_single_fgrn'),
    path('display_FGRN_items', views.display_FGRN_items, name='display_FGRN_items'),
    path('inventory_fgrn_items/manage', line_portal_views.manage_inventory_fgrn_items, name='manage_inventory_fgrn_items'),
    path('inventory_fgrn_items/manage/add', line_portal_views.manage_inventory_fgrn_items_add, name='manage_inventory_fgrn_items_add'),
]
