from django.shortcuts import render
from django.http import JsonResponse
from .utils.chatgpt import get_chatgpt_recommendations, get_chatgpt_recommendations_plain


def gpt_enhance(request):
    if request.method == 'POST':
        original_markdown = request.POST.get('markup')
        model = request.POST.get('gpt_model')
        print("=======FORM GPT MODEL========" + model + "========GPT MODEL=======")
        print("-----------Original Markdown-------------\n\n\n\n " + original_markdown + "-------------   END OF ORIGINAL ----------")
        enhanced_markdown = get_chatgpt_recommendations(original_markdown, model)
        print("========   From ChatGPT:   ===========\n\n" + enhanced_markdown + "\n\n ========   END OF GPT RESPONSE ===========")
        return JsonResponse({'enhanced_markdown': enhanced_markdown})
    return JsonResponse({'error': 'Invalid request'}, status=400)

