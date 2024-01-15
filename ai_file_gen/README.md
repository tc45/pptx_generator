# Django Outline-to-PowerPoint (DOTP) Project

The DOTP project is a Django-based web application designed to create enhanced PowerPoint presentations from markdown outlines. It leverages OpenAI's ChatGPT to interpret and add contextual information and notes to outlines, thereby generating enriched content for your presentations.

## Quickstart Guide

### Prerequisites

Before starting, ensure that you have Python v3.11.7 and Django installed.

Python can be downloaded and installed from the [official Python website](https://www.python.org/downloads/).

Once Python is installed, you can install Django using pip:

### Setting Up the DOTP Project

To get the DOTP project running on your local machine, follow these steps:

1. Clone the DOTP repository:
    - bash git clone https://github.com/tc45/pptx_generator.git
2. Move into the project directory:
    bash cd powerpoint_tools
3. Install the necessary packages:
    bash pip install -r requirements.txt

### Launching the Project

Start the Django server using the following command:
You can now access the application on your browser at http://127.0.0.1:8000/.

### Using DOTP

Upon launching the web application, you can input your PowerPoint outline in markdown format. The application will send this outline to ChatGPT, which will fill it with context-specific texts, notes, and more to enrich your presentation. The final enhanced outline will be saved locally on your machine.

## Built With

- [Django](https://www.djangoproject.com/): The web framework used.
- [ChatGPT](https://www.openai.com/gpt-3/): AI model for text generation.

## Contributing

For contributing to this project, please fork the repository, make your updates and create a pull request.

## License

Provide information about your project's licensing here.

## Acknowledgments

Include acknowledgments for the contributors or references you have used in your project.