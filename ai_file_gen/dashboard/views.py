from django.shortcuts import render
def index(request):
    # View for the index page of the PowerPoint Generator app
    return render(request, 'dashboard/index.html')

