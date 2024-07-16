from django.contrib import admin
from django.urls import path, include
from FGRN import views
urlpatterns = [
    path('create_fgrn', views.create_fgrn, name='create_fgrn'),
    path('display_goods', views.display_goods, name='display_goods'),
    path('create_fgrn_items', views.create_fgrn_items, name='create_fgrn_items'),
    path('display_FGRN', views.display_FGRN, name='display_fgrn'),
]