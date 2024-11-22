from django.contrib import admin
from django.urls import path, include
from FGRN import views
urlpatterns = [
    path('create_fgrn', views.create_fgrn, name='create_fgrn'),
    path('display_goods', views.display_goods, name='display_goods'),
    # path('create_fgrn_items', views.create_fgrn_items, name='create_fgrn_items'),
    path('display_FGRN', views.display_FGRN, name='display_fgrn'),
    path('fgrn_opening_balance', views.fgrn_opening_balances, name='fgrn_opening_balance'),
    path('display_single_fgrn', views.display_single_fgrn, name='display_single_fgrn'),
    path('display_FGRN_items', views.display_FGRN_items, name='display_FGRN_items'),
    path('create_group/', views.create_group, name='create_group'),
]