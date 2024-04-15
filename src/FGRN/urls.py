from django.urls import path
from . import views

urlpatterns = [
    path('fgrn_base/', views.fgrn_base, name='fgrn_base')
]
