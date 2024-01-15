from django.urls import path, include
from . import views

urlpatterns = [
    path('gpt_enhance/', views.gpt_enhance, name='gpt_enhance'),
    path('gpt_input_prompt/', views.gpt_input_prompt, name='gpt_input_prompt'),
    path('jupyter_notes/', views.JupyterNoteView.as_view(), name='jupyter_note'),
    # path('gpt_enhance/<str:model>', views.gpt_enhance, name='gpt_enhance'),
]
