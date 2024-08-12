
from django.urls import path, include
from MR import views
urlpatterns = [
    path('create_MR', views.create_MR,name= 'create_MR'),
    path('create_MR_items',views.create_MR_items, name= 'create_MR_items'),
    path('display_MR',views.display_MR, name= 'display_MR'),
    path('display_inventory',views.display_inventory, name= 'display_inventory'),
    path('opening_balances',views.opening_balances, name= 'opening_balances'),
    path('display_single_mr',views.display_single_mr, name= 'display_single_mr'),
    path('display_MR_items',views.display_MR_items, name= 'display_MR_items'),

]