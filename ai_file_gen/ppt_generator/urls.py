from django.urls import path
from . import views

urlpatterns = [
    # URL configuration for the Theme Applier app
    path('', views.index, name='index'),  # Assuming a view named 'index' in views.py
    #path('markdown_to_pptx/', views.markdown_to_pptx, name='markdown_to_pptx'),  # New URL for creating PPTX
    path('save_presentation/', views.save_presentation, name='save_presentation'),
]
