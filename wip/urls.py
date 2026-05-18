from django.urls import path

from . import views

urlpatterns = [
    path('create_WIP', views.create_wip, name='create_WIP'),
    path('display_WIP', views.display_wip, name='display_WIP'),
    path(
        'api/flow_item_suggestions',
        views.mrfwip_flow_item_suggestions,
        name='mrfwip_flow_item_suggestions',
    ),
    path(
        'MR_WIP_FGRN_difference',
        views.mrfwip_fgrn_flow_difference,
        name='mrfwip_fgrn_flow_difference',
    ),
]
