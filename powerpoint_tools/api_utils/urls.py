from django.urls import path
from . import views

urlpatterns = [
    path('gpt_enhance/', views.gpt_enhance, name='gpt_enhance'),
    # path('gpt_enhance/<str:model>', views.gpt_enhance, name='gpt_enhance'),
]
