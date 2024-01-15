from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views import View
from .utils.chatgpt import get_chatgpt_recommendations, get_chatgpt_recommendations_plain, get_gpt_prompt
from .utils.jupyter_utils import markdown_to_ipynb, execute_notebook
import logging

logger = logging.getLogger(__name__)


def gpt_enhance_old(request):
    logger.info('Running gpt_enhance module  from api_utils/views.py.')
    if request.method == 'POST':
        original_markdown = request.POST.get('markup')
        model = request.POST.get('gpt_model')
        logger.info(f"GPT Model Chosen: " + model)
        logger.info(f"Original Markdown: \n" + original_markdown + "\n\n---------------------------------")
        enhanced_markdown = get_chatgpt_recommendations(original_markdown, model)
        logger.info(f"Response from GPT: \n\n" + enhanced_markdown + "\n\n---------------------------------")
        return JsonResponse({'enhanced_markdown': enhanced_markdown})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def gpt_input_prompt_old(request):
    logger.info("Running gpt_input_prompt from api_utils/views.py.")
    if request.method == 'POST':
        user_input = request.POST.get('userInput')
        model = request.POST.get('gpt_model')
        logger.info("=======FORM GPT MODEL========" + model + "========GPT MODEL=======")
        logger.info("-----------Original Markdown-------------\n\n " + user_input + "\n\n-------------   END OF ORIGINAL ----------")
        enhanced_markdown = get_gpt_prompt(user_input, model)
        logger.info("========   From ChatGPT:   ===========\n\n" + enhanced_markdown + "\n\n ========   END OF GPT RESPONSE ===========")
        return JsonResponse({'enhanced_markdown': enhanced_markdown})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def process_gpt_request(request, process_type):
    """
    Processes the request for GPT enhancement or GPT input prompt

    Args:
        request (HTTPRequest):       The client request to handle
        process_type (str):      Defines the type of process to execute. Can be 'enhance' or 'input_prompt'

    Returns:
        JsonResponse: Json Response to be output
    """
    # Running the module from api_utils/views.py.
    logger.info(f"Running {process_type} from api_utils/views.py.")

    if request.method == 'POST':
        model = request.POST.get('gpt_model')
        logger.info("GPT Model Chosen: " + model)
        enhanced_markdown = ""

        if process_type == 'enhance':
            original_markdown = request.POST.get('markup')
            logger.info(f"Original Markdown: \n{original_markdown}\n\n---------------------------------")
            enhanced_markdown = get_chatgpt_recommendations(original_markdown, model)
        elif process_type == 'input_prompt':
            user_input = request.POST.get('userInput')
            logger.info("Original Markdown:\n\n " + user_input + "\n\n-------------   END OF ORIGINAL ----------")
            enhanced_markdown = get_gpt_prompt(user_input, model)

        logger.info(f"Response from GPT: \n\n{enhanced_markdown}\n\n---------------------------------")
        return JsonResponse({'enhanced_markdown': enhanced_markdown})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def gpt_enhance(request):
    """
    Handles the requests for GPT enhancement

    Args:
        request (HTTPRequest):       The client request to handle

    Returns:
        JsonResponse: Json Response to be output
    """
    return process_gpt_request(request, 'enhance')


def gpt_input_prompt(request):
    logger.info("Executing the gpt_input_prompt from api_utils/views.py")
    """
    Handles the requests for GPT input prompt

    Args:
        request (HTTPRequest):       The client request to handle

    Returns:
       JsonResponse: Json Response to be output
    """
    return process_gpt_request(request, 'input_prompt')


class JupyterNoteView(View):
    """
    Django View that converts the markdown content sent in a POST request to a Jupyter notebook.
    The notebook is executed, and a notebook (.ipynb) is returned as a response.

    Methods
    -------
    post(request, *args, **kwargs):
        Takes as input a request that contains markdown content in json format {'markdown': '# example markdown'}.
        Converts the markdown to a Jupyter notebook and runs the notebook cells.
        The executed notebook is then exported as html and .ipynb file. The rendered HTML is then returned.
    """

    def post(self, request, *args, **kwargs):
        markdown_content = request.json.get('markdown')
        notebook = markdown_to_ipynb(markdown_content)
        html_data, notebook_data = execute_notebook(notebook)
        return HttpResponse(html_data, content_type='application/octet-stream')
