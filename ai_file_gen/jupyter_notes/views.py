from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'jupyter_notes/index.html')

# def index(request):
#     return render(request, 'jupyter_notes/index.html')
