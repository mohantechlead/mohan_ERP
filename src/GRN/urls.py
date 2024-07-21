from django.contrib import admin
from django.urls import path, include
from GRN import views
urlpatterns = [
    # path('display_items/<str:pr_no>/', views.display_items, name='display_items'),
    # path('create_items', views.create_items, name='create_items'),
    path('create_grn', views.create_grn, name='create_grn'),
    path('create_grn_items', views.create_grn_items, name='create_grn_items'),
    # path('display_pr', views.display_pr, name='display_pr'),
    path('display_search_items', views.display_search_items, name='display_search_items'),
    path('display_grn', views.display_grn, name='display_grn'),
    path('display_grns', views.display_grns, name='display_grns'),
    path('search_prs/<str:grn_no>/', views.search_prs, name='search_prs'),
    path('print_format', views.print_format, name='print_format'),
    path('print_pr', views.print_pr, name='print_pr'),
    path('search_pr_item', views.search_pr_item, name='search_pr_item'),
    path('search_customer', views.search_customer, name='search_customer'),
    path('search_items', views.search_items, name='search_items'),
    path('create_trial_grn', views.create_trial_grn, name='create_trial_grn'),
    path('grn_number', views.grn_number, name='grn_number'),
    # path('admin/custom-report-page/', views.custom_report_page, name='custom_report_page'),
    path('search_grns', views.search_grns, name='search_grns'),
]


