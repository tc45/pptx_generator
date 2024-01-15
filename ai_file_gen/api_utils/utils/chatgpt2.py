import requests
import os
import re
from openai import OpenAI, OpenAIError
from decouple import config


def call_chatgpt_api(in_prompt, content, model="gpt-3.5-turbo"):
    """Call the GPT-3 API to get recommendations for provided content."""

    api_key_env = config('GPT_API_KEY')
    if not api_key_env:
        raise ValueError("GPT API key not found in environment variables")
    client = OpenAI(api_key=api_key_env)

    content = in_prompt + "\n\n" + content
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system",
                 "content": ("You are an expert in automation "
                             "and delivering a presentation to other engineers who do not understand it.")},
                {"role": "user", "content": content},
            ],
            stream=True)
        collected_messages = [chunk.choices[0].delta.content for chunk in stream
                              if chunk.choices[0].delta.content is not None]

        return "".join(collected_messages)
    except OpenAIError as e:
        return f"Error: {str(e)}"


def get_chatgpt_recommendations(markdown_content, model):
    """Process Markdown content and get recommendations."""

    slides = re.findall(r'(## .+?)(?=## |\Z)', markdown_content, flags=re.S)
    input_prompt = """
    DO NOT CHANGE ANY EXISTING MARKDOWN FOR TITLES, HEADERS, BULLETS, or Notes (denoted by <!-- -->). H1 is title slides, h2 is subtitle slides, h3 is regular slides, and <!-- --> is notes. Keep all original slide titles and bullet points.
    """
    updated_slides = [call_chatgpt_api(input_prompt, slide, model=model) for slide in slides]

    return "\n\n".join(updated_slides)


def get_chatgpt_recommendations_plain(text):
    """Process plain text and get recommendations."""

    input_prompt = """
    Consider that my target audience is internal training for a technical team of network engineers.
    Below is the contents for the slide:
    """
    updated_text = call_chatgpt_api(input_prompt, text)

    return updated_text