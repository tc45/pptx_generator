from django.shortcuts import render
from django.http import HttpResponse
from .utils import generate_pptx as gpptx
from .forms import pptx_markdown


def index(request):
    form = pptx_markdown()
    # View for the index page of the PowerPoint Generator app
    return render(request, 'ppt_generator/index.html', {'form': form})


def save_presentation(request):
    form = pptx_markdown()
    if request.method == 'POST':
        markdown = request.POST.get('markup')
        filename = request.POST.get('outputPath')
        print(filename)
        pptx_content, new_file = gpptx.save_presentation(markdown, filename, format="bytes")  # Generate PPTX from markup
        # print(new_file)
        # Create a response with the PPTX file
        response = HttpResponse(pptx_content.getvalue(), content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
        response['Content-Disposition'] = f'attachment; filename="{new_file}"'
        return response
    return render(request, 'ppt_generator/index.html', {'form': form})
