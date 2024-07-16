
from django.urls import path, include
from MR import views
urlpatterns = [
    path('create_MR', views.create_MR,name= 'create_MR'),
    path('create_MR_items',views.create_MR_items, name= 'create_MR_items'),
    path('display_MR',views.display_MR, name= 'display_MR'),
    path('display_inventory',views.display_inventory, name= 'display_inventory'), 
]