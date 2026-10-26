# Azure Course Helper Bot

An FAQ chatbot built using Python, Azure AI Search, and Streamlit. It helps students find answers to Azure and course-related questions from a predefined FAQ dataset.

## Features

- Search course-related FAQs using Azure AI Search
- Display relevant answers in a simple chat interface
- Show the matched FAQ question
- Optional Urdu translation support through Azure Translator

## Tech Stack

- Python
- Azure AI Search
- Streamlit
- REST API
- Python-dotenv

## Project Files

- `chatbot.py` — Streamlit chatbot interface
- `ask.py` — Tests FAQ search functionality
- `load_faq.py` — Creates the search index and uploads FAQ data
- `faq.json` — FAQ dataset
- `requirements.txt` — Python dependencies
- `.gitignore` — Excludes sensitive and unnecessary files

## Setup

1. Clone or download this repository.
2. Install the dependencies:

   `pip install -r requirements.txt`

3. Create a local `.env` file using the following format:

   `SEARCH_ENDPOINT=your_azure_search_endpoint`

   `SEARCH_KEY=your_azure_search_key`

   `TRANSLATOR_KEY=`

   `TRANSLATOR_REGION=eastus`

4. Configure your Azure AI Search service and ensure the `faq` index contains the FAQ dataset.
5. Run the chatbot:

   `python -m streamlit run chatbot.py`

## Security

Never upload API keys, `.env` files, or other secrets to GitHub.

## Project Status

Built as a learning project to practice Azure AI Search integration, API requests, and Streamlit application development.
