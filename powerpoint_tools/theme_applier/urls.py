from django.urls import path
from . import views

urlpatterns = [
    # URL configuration for the Theme Applier app
    path('', views.index, name='index'),  # Assuming a view named 'index' in views.py
]
