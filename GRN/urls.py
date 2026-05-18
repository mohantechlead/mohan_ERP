from django.contrib import admin
from django.urls import path, include
from GRN import views
from GRN import vendor_payment_views

urlpatterns = [
    # path('display_items/<str:pr_no>/', views.display_items, name='display_items'),
    # path('create_items', views.create_items, name='create_items'),
    path('create_grn', views.create_grn, name='create_grn'),
    path('create_grn_items', views.create_grn_items, name='create_grn_items'),
    path('create_pr', views.create_pr, name='create_pr'),
    path('create_actual_purchase', views.create_actual_purchase, name='create_actual_purchase'),
    path('display_actual_purchases', views.display_actual_purchases, name='display_actual_purchases'),
    path('actual-purchase/<uuid:actual_purchase_id>', views.actual_purchase_detail, name='actual_purchase_detail'),
    path('get_actual_purchase_pr_items', views.get_actual_purchase_pr_items, name='get_actual_purchase_pr_items'),
    path('purchase_difference', views.purchase_difference, name='purchase_difference'),
    path('create_items', views.create_items, name='create_items'),
    path('display_pr', views.display_pr, name='display_pr'),
    # path('display_single_grn', views.display_single_grn, name='display_single_grn'),
    path('display_single_grn/<str:GRN_no>', views.display_single_grn, name='display_single_grn'),
    path('display_search_items', views.display_search_items, name='display_search_items'),
    path('display_grn', views.display_grn, name='display_grn'),
    path('display_grn_item', views.display_grn_item, name='display_grn_item'),
    path('display_grns', views.display_grns, name='display_grns'),
    path('print_format', views.print_format, name='print_format'),
    path('print_pr/<str:PR_no>', views.print_pr, name='print_pr'), 
    path('search_customer', views.search_customer, name='search_customer'),
    path('search_items', views.search_items, name='search_items'),
    path('create_trial_grn', views.create_trial_grn, name='create_trial_grn'),
    path('create_import_grn', views.create_import_grn, name='create_import_grn'),
    path('create_import_grn_items', views.create_import_grn_items, name='create_import_grn_items'),
    path('grn_number', views.grn_number, name='grn_number'),
    # path('admin/custom-report-page/', views.custom_report_page, name='custom_report_page'),
    path('search_grns', views.search_grns, name='search_grns'),
    path('create_supplier', views.create_supplier, name="create_supplier"),
    path('display_supplier', views.display_supplier, name="display_supplier"),
    path('send_email_reminder', views.send_email_reminder, name='send_email_reminder'),
     path('supplier/<str:company>/', views.supplier_details, name='supplier_details'),

    path('vendor-payments/create', vendor_payment_views.create_vendor_payment, name='create_vendor_payment'),
    path('vendor-payments/display', vendor_payment_views.display_vendor_payments, name='display_vendor_payments'),
    path('vendor-payments/completed', vendor_payment_views.vendor_payments_completed, name='vendor_payments_completed'),
    path('vendor-payments/rejected', vendor_payment_views.vendor_payments_rejected, name='vendor_payments_rejected'),
    path('vendor-payments/approvals', vendor_payment_views.vendor_payment_approvals, name='vendor_payment_approvals'),
    path('vendor-payments/status', vendor_payment_views.vendor_payment_status, name='vendor_payment_status'),
    path('vendor-payments/purchase/<path:pr_no>', vendor_payment_views.vendor_payment_purchase_summary, name='vendor_payment_purchase_summary'),
    path('vendor-payments/bulk-approve', vendor_payment_views.approve_vendor_payments_bulk, name='approve_vendor_payments_bulk'),
    path('vendor-payments/<path:payment_number>/edit', vendor_payment_views.edit_vendor_payment, name='edit_vendor_payment'),
    path('vendor-payments/<path:payment_number>/delete', vendor_payment_views.delete_vendor_payment, name='delete_vendor_payment'),
    path('vendor-payments/<path:payment_number>/approve', vendor_payment_views.approve_vendor_payment, name='approve_vendor_payment'),
    path('vendor-payments/<path:payment_number>/update-status', vendor_payment_views.update_vendor_payment_status, name='update_vendor_payment_status'),
    path('vendor-payments/<path:payment_number>', vendor_payment_views.vendor_payment_detail, name='vendor_payment_detail'),

]


