"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from DN import views

urlpatterns = [
    path('input_delivery/', views.input_delivery, name='input_delivery'), 
    path('generate-excel/', views.generate_excel, name='generate_excel'),
    path('deliveries_excel/', views.deliveries_excel, name='deliveries_excel'),
    path('display_DN_items', views.display_DN_items, name='display_DN_items'),
    path('display_orders/', views.display_orders, name='display_orders'),
    path('input_orders_items/',views.input_orders_items, name='input_orders_items'),
    path('input_delivery_items/',views.input_delivery_items, name='input_delivery_items'),
     path('display_order_items/',views.display_order_items, name='display_order_items'),
    path('input_orders/', views.input_orders, name='input_orders'),
    path('input_delivery', views.input_delivery, name='input_delivery'),
    path('display_delivery/', views.display_delivery, name='display_delivery'),
    path('deliveries/', views.deliveries, name='deliveries'),   
    path('search_orders/', views.search_orders, name='search_orders'),
    path('search_delivery/', views.search_delivery, name='search_delivery'),
    path('search_customer/', views.search_customer, name='search_customer'),
    path('display_remaining/', views.display_remaining, name='display_remaining'),
    path('order_chart/', views.order_chart, name='order_chart'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('search_customer_delivery/', views.search_customer_delivery, name='search_customer_delivery'),
    path('display_single_order/<str:serial_no>/', views.display_single_order, name='display_single_order'), 
    path('display_single_delivery/<str:delivery_number>', views.display_single_delivery, name='display_single_delivery'), 
    path('customers/', views.customer_list, name='customer_list'),
    path('pivot/', views.dashboard_with_pivot, name='dashboard_with_pivot'),
    path('data', views.pivot_data, name='pivot_data'),
    path('dashboards/', views.dashboards, name='dashboards'),
    path('tables/', views.customer_table, name='tables'),
    path('items/', views.item_table, name='items'),
    path('order_api/',views.order_list),
    path('delivery_api/',views.delivery_list),
    path('sales_contract/',views.sales_contract),
    path('get_order_items/', views.get_order_items, name='get_order_items'),
    path('customer/<str:company>/', views.customer_detail, name='customer_detail'),

]   

