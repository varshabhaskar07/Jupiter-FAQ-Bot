# Jupiter FAQ Bot

This project implements a Streamlit-based FAQ bot for Jupiter, designed to answer user queries by leveraging web scraping, text preprocessing, sentence embeddings, and a large language model (LLM) for rephrasing answers.

## Features

- **Web Scraping**: Automatically extracts FAQs from the Jupiter website using Selenium and BeautifulSoup.
- **Text Preprocessing**: Cleans and normalizes scraped FAQ data, including handling specific text formatting issues like email addresses.
- **Sentence Embeddings**: Uses `SentenceTransformer` to convert questions and answers into numerical embeddings for efficient similarity search.
- **Semantic Search**: Finds the most relevant FAQ entry based on the semantic similarity between the user's query and the preprocessed FAQs.
- **LLM Integration**: Rephrases the matched answers using a Gemini 1.5 Flash model to provide more natural and user-friendly responses.
- **Streamlit UI**: Provides an interactive web interface for users to ask questions and receive answers.

## Setup and Installation

Follow these steps to set up and run the Jupiter FAQ Bot on your local machine.

### Prerequisites

- Python 3.8+
- `pip` (Python package installer)
- Google Chrome browser (for Selenium web scraping)
- ChromeDriver compatible with your Chrome browser version. You can download it from [here](https://chromedriver.chromium.org/downloads).

### 1. Clone the Repository (if applicable)

If your project is in a Git repository, clone it first:

```bash
git clone <your-repository-url>
cd <your-repository-name>