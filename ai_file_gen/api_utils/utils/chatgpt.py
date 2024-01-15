import re
from openai import OpenAI, OpenAIError
import logging
from decouple import config
import matplotlib.pyplot as plt
from wordcloud import WordCloud

logger = logging.getLogger(__name__)

def generate_wordcloud(text, slide_title):
    logger.info("Running generate_wordcloud from api_utils/utils/chatgpt.py")
    wordcloud = WordCloud().generate(text)
    # Display the Image
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    # Save the Image
    plt.savefig(f"{slide_title}.png")


# Function to call the ChatGPT API
def call_chatgpt_api(in_prompt, content, model="gpt-3.5-turbo"):
    logger.info("Running call_chatgpt_api from api_utils/utils/chatgpt.py")
    # Load the API key from environment variable
    api_key_env = config('GPT_API_KEY')
    if not api_key_env:
        raise ValueError("GPT API key not found in environment variables\n")
    api_key = api_key_env
    client = OpenAI(api_key=api_key)
    response = None
    content = in_prompt + "\n\n" + content
    logger.info("Sending prompt to GPT: \n\n" + content + "\n\n\n\n")
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
        logger.info("Beginning Chunking Streams to GPT")
        for chunk in stream:
            logger.info(f"Sending chunk {chunk}")
            if chunk.choices[0].delta.content is not None:
                collected_messages.append(chunk.choices[0].delta.content)
                logger.debug(chunk.choices[0].delta.content)
        content = "".join(collected_messages)
        #logger.info("\n\nChunked content: \n-----------------\n" + content + "\n\n\n\n\n")
        logger.info(f"\n\n\nCollected messages: \n-----------------\n{content}")
        return content if collected_messages else ''
    except OpenAIError as e:
        return f"Error: {str(e)}"


# Function to process Markdown and get recommendations
def get_chatgpt_recommendations(markdown_content, model):
    logger.info("Running get_chatgpt_recommendations from api_utils/utils/chatgpt.py")
    logger.info("============MARKDOWN===========\n\n\n" + markdown_content + "\n\n\n===========MARKDOWN============\n\n")
    # Regex to find H2 headings and corresponding content
    slides = re.findall(r'(## .+?)(?=## |\Z)', markdown_content, flags=re.S)
    #slides = re.findall(r'## (.+?)(?=## |\Z)', markdown_content, flags=re.S)
    #logger.info("========== ORIGINAL SLIDES ========== \n\n\n" + markdown_content + "========== ORIGINAL SLIDES ==========\n\n\n ")
    input_prompt = """
    I need to edit some markdown used to make a powerpoint presentation.  H1 is title, H2 and H3 are individual slides. 
    DO NOT CHANGE ANY EXISTING MARKDOWN FOR TITLES, HEADERS, BULLETS, or Notes (denoted by <!-- -->). H1 is the title, H2 is the headers for each section.  Keep all H2 headers and bullets/paragraphs for H2 in your reply.  
    The other elements (bullets, sub-bullets, paragraphs, notes) should be elaborated on in a technical detailed but concise manner.  
    If necessary, keep bullets under H2 but may also create H3 references to the same bullet and then elaborate on them individually with bullets, paragraphs, and notes.   Limit to 10-25 words per bullet.
    Add very detailed verbose notes to end of each H2 and H3 section in a bulleted list that covers all points generated. Include suggestions on how to enhance the slide. Start notes with <!-- and end with -->.        
    """
    updated_slides = []
    logger.info("\n\n\nModel is: " + model + "\n\n\n")
    for slide in slides:
        logger.info("---------------NEXT SLIDE-------------\n\n\n")
        logger.info(slide + "\n\n\n ------------ END SLIDE -------------")
        recommendation = call_chatgpt_api(input_prompt, slide, model=model)
        #logger.info("From API Call:\n---------------\n" + recommendation + "--------------- End of API Call -----------")
        updated_slides.append(recommendation)
        generate_wordcloud(slide, f"Slide_{slides.index(slide)}")

    # Reconstruct the updated Markdown
    updated_markdown = "\n\n".join(updated_slides)
    return updated_markdown


def get_chatgpt_recommendations_plain(text, model):
    logger.info("Running get_chatgpt_recommendations_plain from api_utils/utils/chatgpt.py")
    # Regex to find H2 headings and corresponding content
    #slides = re.findall(r'## (.+?)(?=## |\Z)', markdown_content, flags=re.S)
    input_prompt = f"""
    The user wants to create an outline of a Jupyter Notebook based on the following prompt.  
    Generate a response in structured markdown suitable for a jupyter notebook. 
    Each section should have text as well as code samples that illustrate the functionality..
    """
    updated_text = []
    recommendation = call_chatgpt_api(input_prompt, text, model)
    logger.info("From API Call:\n---------------\n" + recommendation + "--------------- End of API Call -----------")
    updated_text.append(recommendation)

    # Reconstruct the updated Markdown
    updated_text = "\n\n".join(updated_text)
    return updated_text


def get_gpt_prompt(user_input, model):
    logger.info("Running get_gpt_prompt from api_utils/utils/chatgpt.py")
    # Modify input_prompt to suit your needs
    logger.info(f"User input: {user_input}")
    # input_prompt = f"""
    # The user asked the following question: `{user_input}`.
    # Generate a response in structured markdown suitable for a powerpoint presentation slide.
    # Convert the question into a header, followed by bullets with detailed and concise information.
    # """

    input_prompt = f"""
    The user wants to create an outline of a Jupyter Notebook based on the following prompt.  
     \n\n`{user_input}`.\n\n 
    Generate a response in structured markdown suitable for a jupyter notebook. 
    Each section should have text as well as code samples that illustrate the functionality..
    """

    # Call the ChatGPT API
    response = get_chatgpt_recommendations_plain(input_prompt, model=model)
    print(response)
    logging.info(f"Preprocessed response received from GPT: \n\n{response}")
    # Format the response in Markdown
    heading = f"## {response}\n"
    bullets = re.findall(r"(?<=\-\s)(.*?)(?=\n)", response)  # Extracting bullet points
    bullets_md = '\n'.join([f"- {bullet}" for bullet in bullets])  # Constructing bullet points in Markdown
    markdown_response = f"{heading}{bullets_md}"
    logging.info(f'Markdown edit: \n\n {markdown_response}')
    return markdown_response
