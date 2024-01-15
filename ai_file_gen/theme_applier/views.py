from django.shortcuts import render
def index(request):
    # View for the index page of the Theme Applier app
    return render(request, 'theme_applier/index.html')

