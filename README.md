# Jupiter FAQ Bot

This project implements a Streamlit-based FAQ 
bot for Jupiter, designed to answer user 
queries by leveraging web scraping, text 
preprocessing, sentence embeddings, and a large 
language model (LLM) for rephrasing answers.

## Features

- **Web Scraping**: Automatically extracts FAQs 
from the Jupiter website using Selenium and 
BeautifulSoup.
- **Text Preprocessing**: Cleans and normalizes 
scraped FAQ data, including handling specific 
text formatting issues like email addresses.
- **Sentence Embeddings**: Uses 
`SentenceTransformer` to convert questions and 
answers into numerical embeddings for efficient 
similarity search.
- **Semantic Search**: Finds the most relevant 
FAQ entry based on the semantic similarity 
between the user's query and the preprocessed 
FAQs.
- **LLM Integration**: Rephrases the matched 
answers using a Gemini 1.5 Flash model to 
provide more natural and user-friendly 
responses.
- **Streamlit UI**: Provides an interactive web 
interface for users to ask questions and 
receive answers.

## Setup and Installation

Follow these steps to set up and run the 
Jupiter FAQ Bot on your local machine.

### Prerequisites

- Python 3.8+
- `pip` (Python package installer)
- Google Chrome browser (for Selenium web 
scraping)
- ChromeDriver compatible with your Chrome 
browser version. You can download it from [here]
(https://chromedriver.chromium.org/downloads).

### 1. Clone the Repository (if applicable)

If your project is in a Git repository, clone 
it first:

```bash
git clone <your-repository-url>
cd <your-repository-name>
```
### 2. Create a Virtual Environment
It's highly recommended to use a virtual environment to manage dependencies.

### 3. Activate the Virtual Environment
On Windows:

On macOS/Linux:

### 4. Install Dependencies
Install all required Python packages using pip :

If you don't have a requirements.txt file, you can create one with the following content and then run the command above:

### 5. Set up ChromeDriver
Ensure that chromedriver.exe (or chromedriver on macOS/Linux) is placed in a location accessible by the script. The current script expects it at C:\chromedriver-win64\chromedriver.exe .

Update the scrape_faqs function in jupiter_faq_bot.py if your ChromeDriver path is different:

### 6. Obtain a Gemini API Key
To use the LLM rephrasing feature, you need a Google Gemini API key. You can obtain one from the Google AI Studio .

Update the GEMINI_API_KEY in the main function of jupiter_faq_bot.py :

## Usage
### 1. Scrape and Preprocess FAQs (First Time Setup / Data Refresh)
Before running the Streamlit app for the first time, or whenever you want to refresh the FAQ data, you need to run the scraping and preprocessing steps. These lines are commented out by default in jupiter_faq_bot.py to prevent accidental re-scraping.

Uncomment the following lines in the if __name__ == "__main__": block of jupiter_faq_bot.py :

Then, run the script from your terminal:

This will:

- Scrape FAQs from jupiter.money/contact/ and save them to jupiter_faqs.csv .
- Preprocess the FAQs and save the cleaned data to jupiter_faqs_preprocessed.csv .
Important : After jupiter_faqs_preprocessed.csv is generated, re-comment these two lines ( df = scrape_faqs() and df = preprocess_faqs(df) ) to avoid re-scraping every time you run the Streamlit app.

### 2. Run the Streamlit Application
Once the jupiter_faqs_preprocessed.csv file is generated, you can run the Streamlit application. Ensure the scraping and preprocessing lines are commented out as instructed above.

This command will open the Streamlit application in your web browser, typically at http://localhost:8501 .

## Project Structure
## Troubleshooting
- FileNotFoundError: jupiter_faqs_preprocessed.csv : Ensure you have run the scraping and preprocessing steps as described in "Usage" section.
- NotImplementedError: torch.nn.Module.to() : This indicates a potential issue with the SentenceTransformer model trying to load to a GPU device that isn't available or properly configured. The current code explicitly loads the model to CPU, which should resolve this. If it persists, ensure your sentence-transformers library is up to date.
- Incorrect Email Formatting : If the bot provides email addresses like support@jupiter.moneyor or atsupport@jupiter.money , ensure you have the latest clean_text function in preprocess_faqs and have re-run the scraping and preprocessing steps.
- AttributeError: 'FAQBot' object has no attribute 'rephrase_answer_with_llm' : This indicates the rephrase_answer_with_llm method is missing or incorrectly defined in the FAQBot class. Ensure your jupiter_faq_bot.py includes this method as provided in the solution.
- Selenium WebDriver Issues : If you encounter issues with Chrome or ChromeDriver, ensure:
  - Chrome browser is installed and up to date.
  - ChromeDriver version matches your Chrome browser version.
  - ChromeDriver executable path in scrape_faqs is correct.
If you encounter any other issues, please refer to the console output for error messages and consider checking the official documentation for the libraries used (Selenium, BeautifulSoup, pandas, sentence-transformers, google-generativeai, Streamlit).
