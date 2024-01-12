import requests
from tenacity import retry, stop_after_attempt, wait_fixed
import re
import os
from openai import OpenAI, api_key, OpenAIError
import openai

from decouple import config

import matplotlib.pyplot as plt
from wordcloud import WordCloud


def generate_wordcloud(text, slide_title):
    wordcloud = WordCloud().generate(text)
    # Display the Image
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    # Save the Image
    plt.savefig(f"{slide_title}.png")



# Function to call the ChatGPT API
def call_chatgpt_api(in_prompt, content, model="gpt-3.5-turbo"):
    # Load the API key from environment variable
    api_key_env = config('GPT_API_KEY')
    if not api_key_env:
        raise ValueError("GPT API key not found in environment variables\n")

    api_key = api_key_env
    client = OpenAI(api_key=api_key)
    response = None
    print("----------CONTENT------------\n\n\n" + content + "\n\n\n------------CONTENT----------\n\n\n")
    content = in_prompt + "\n\n" + content
    print("Input prompt: " + content + "\n\n\n\n")
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system",
                 "content": "You are an expert in automation and delivering a presentation to other engineers who do "
                            "not understand it."},
                #{"role": "user", "content": in_prompt},
                {"role": "user", "content": content},

            ],
            stream=True)

        collected_messages = []
        print("Chunking Streams")
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                collected_messages.append(chunk.choices[0].delta.content)
                print(chunk.choices[0].delta.content, end="")
        content = "".join(collected_messages)
        #print("\n\nChunked content: \n-----------------\n" + content + "\n\n\n\n\n")
        print("\n\n\nCollected messages: \n-----------------\n" + "".join(collected_messages))
        return content if collected_messages else ''
    except OpenAIError as e:
        return f"Error: {str(e)}"

    #     for chunk in stream:
    #         response = chunk
    #         print(response)
    #         if response.choices[0].delta.content is not None:
    #             print(response.choices[0].delta.content, end="")
    #     return response.choices[0].text.strip() if response.choices and response else ''
    # except openai.OpenAIError as e:
    #     return f"Error: {str(e)}"

# @retry(stop=stop_after_attempt(3), wait=wait_fixed(30))
# def call_chatgpt_api_original(in_prompt, slide_data):
#     api_endpoint = "https://api.openai.com/v1/engines/davinci-codex/completions"
#
#     # Get the API key from an environment variable
#     api_key = os.environ.get('GPT_API_KEY')
#     if not api_key:
#         raise ValueError("GPT API key not found in environment variables")
#
#     headers = {
#         "Authorization": api_key
#     }
#     new_prompt = in_prompt + "\n\n\n\n" + slide_data
#     data = {
#         "prompt": slide_data,
#         "max_tokens": 150
#     }
#
#     try:
#         response = requests.post(api_endpoint, headers=headers, json=data)
#         response.raise_for_status()
#         return response.json().get('choices', [{}])[0].get('text', '')
#     except requests.RequestException as e:
#         return f"Error: {str(e)}"


# Function to process Markdown and get recommendations
def get_chatgpt_recommendations(markdown_content, model):
    print("============MARKDOWN===========\n\n\n" + markdown_content + "\n\n\n===========MARKDOWN============\n\n")
    # Regex to find H2 headings and corresponding content
    slides = re.findall(r'(## .+?)(?=## |\Z)', markdown_content, flags=re.S)
    #slides = re.findall(r'## (.+?)(?=## |\Z)', markdown_content, flags=re.S)
    #print("========== ORIGINAL SLIDES ========== \n\n\n" + markdown_content + "========== ORIGINAL SLIDES ==========\n\n\n ")
    input_prompt = """
    I need to edit some markdown used to make a powerpoint presentation.  H1 is title, H2 and H3 are individual slides. 
    DO NOT CHANGE ANY EXISTING MARKDOWN FOR TITLES, HEADERS, BULLETS, or Notes (denoted by <!-- -->). H1 is the title, H2 is the headers for each section.  Keep all H2 headers and bullets/paragraphs for H2 in your reply.  
    The other elements (bullets, sub-bullets, paragraphs, notes) should be elaborated on in a technical detailed but concise manner.  
    If necessary, keep bullets under H2 but may also create H3 references to the same bullet and then elaborate on them individually with bullets, paragraphs, and notes.   Limit to 10-25 words per bullet.
    Add very detailed verbose notes to end of each H2 and H3 section in a bulleted list that covers all points generated. Include suggestions on how to enhance the slide. Start notes with <!-- and end with -->.        
    """
    updated_slides = []
    print("\n\n\nModel is: " + model + "\n\n\n")
    for slide in slides:
        print("---------------NEXT SLIDE-------------\n\n\n")
        print(slide + "\n\n\n ------------ END SLIDE -------------")
        recommendation = call_chatgpt_api(input_prompt, slide, model=model)
        #print("From API Call:\n---------------\n" + recommendation + "--------------- End of API Call -----------")
        updated_slides.append(recommendation)
        generate_wordcloud(slide, f"Slide_{slides.index(slide)}")

    # Reconstruct the updated Markdown
    updated_markdown = "\n\n".join(updated_slides)
    return updated_markdown


def get_chatgpt_recommendations_plain(text):
    # Regex to find H2 headings and corresponding content
    #slides = re.findall(r'## (.+?)(?=## |\Z)', markdown_content, flags=re.S)
    print("========== ORIGINAL SLIDES ========== \n\n\n" + text + "\n\n\n ========== END OF ORIGINAL ==========\n\n\n ")
    input_prompt = """
    I am writing a powerpoint presentation and want to enhance it.  Below is the contents for one
    slide of the deck.  Consider that my target audience is internal training for a technical team of network engineers.
    Below is the contents for the slide:\n\n\n 
    """
    updated_text = []
    recommendation = call_chatgpt_api(input_prompt, text)
    print("From API Call:\n---------------\n" + recommendation + "--------------- End of API Call -----------")
    updated_text.append(recommendation)

    # Reconstruct the updated Markdown
    updated_text = "\n\n".join(updated_text)
    return updated_text
