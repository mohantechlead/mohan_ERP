from django.urls import path
from . import views

urlpatterns = [
    path('mr_base/', views.mr_base, name="mr_base" ),  
]