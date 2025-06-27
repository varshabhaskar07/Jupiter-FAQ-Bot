# Jupiter FAQ Bot

This project implements a **Streamlit-based FAQ bot for Jupiter**, designed to answer user queries by leveraging **web scraping**, **text preprocessing**, **sentence embeddings**, and a **large language model (LLM)** for rephrasing answers.

---

## 🚀 Features

- **Web Scraping**: Extracts FAQs from Jupiter’s website using Selenium and BeautifulSoup.
- **Text Preprocessing**: Cleans and formats scraped data, including correcting email formatting.
- **Sentence Embeddings**: Uses `SentenceTransformer` to represent questions/answers as vectors for similarity search.
- **Semantic Search**: Finds the most relevant FAQ entry based on the user's query.
- **LLM Integration**: Rephrases matched answers using Google's Gemini 1.5 Flash for natural responses.
- **Streamlit UI**: Interactive web interface for asking questions and receiving responses.

---

## 🛠️ Setup & Installation

### 🔗 Prerequisites
- Python 3.8+
- `pip` (Python package installer)
- Google Chrome browser
- ChromeDriver (compatible with your Chrome version) — [Download here](https://chromedriver.chromium.org/downloads)

### 🧾 1. Clone the Repository
```bash
git clone https://github.com/varshabhaskar07/Jupiter-FAQ-Bots.git
cd Jupiter-FAQ-Bots
````

### 🧪 2. Create and Activate a Virtual Environment

**Windows:**

```bash
python -m venv env
env\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv env
source env/bin/activate
```

### 📦 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### 🧭 ChromeDriver Path

Ensure `chromedriver.exe` is located at:

```
C:\chromedriver-win64\chromedriver.exe
```

> If not, update the path in `scrape_faqs()` inside `jupiter_faq_bot.py`.

### 🔑 Gemini API Key

To use the LLM rephrasing feature:

1. Get a Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app).
2. Replace `YOUR_GEMINI_API_KEY` in the script with your actual key in the `main()` function.

---

## 💡 Usage

### ✅ 1. Scrape and Preprocess FAQs (Only Once or When Refreshing)

In `jupiter_faq_bot.py`, uncomment the following lines inside the `if __name__ == "__main__":` block:

```python
df = scrape_faqs()
df = preprocess_faqs(df)
```

Then run:

```bash
python jupiter_faq_bot.py
```

This will:

* Scrape data from [jupiter.money/contact](https://jupiter.money/contact)
* Save `jupiter_faqs.csv` and the preprocessed version `jupiter_faqs_preprocessed.csv`

> ⚠️ Important: After running once, **comment those lines again** to avoid re-scraping every time.

---

### ▶️ 2. Run the Streamlit App

```bash
streamlit run jupiter_faq_bot.py
```

This opens the app in your browser (usually at `http://localhost:8501`).

---

## 📁 Project Structure

```
Jupiter-FAQ-Bots/
│
├── jupiter_faq_bot.py             # Main app file
├── jupiter_faqs.csv               # Raw scraped FAQs
├── jupiter_faqs_preprocessed.csv  # Cleaned FAQ data
├── requirements.txt               # Python dependencies
├── .gitignore                     # Ignoring virtual environment
└── README.md                      # Project documentation
```

---

## 🧯 Troubleshooting

* **`FileNotFoundError: jupiter_faqs_preprocessed.csv`**
  → Make sure to run scraping + preprocessing first.

* **`NotImplementedError: torch.nn.Module.to()`**
  → Ensure the SentenceTransformer model is loaded to CPU (this is already done in the code).

* **Malformed Emails (e.g. `support@jupiter.moneyor`)**
  → Update your `clean_text()` function and rerun preprocessing.

* **`AttributeError: 'FAQBot' object has no attribute 'rephrase_answer_with_llm'`**
  → Ensure `rephrase_answer_with_llm()` is defined in your `FAQBot` class.

* **Selenium WebDriver Issues**

  * Confirm Chrome is installed and updated.
  * Match ChromeDriver version to your Chrome.
  * Verify `chromedriver.exe` path is correct in the script.

---

## 📬 Questions or Issues?

If you face any issues, please check the console logs first. You may also consult the documentation for:

* [Selenium](https://selenium-python.readthedocs.io/)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [sentence-transformers](https://www.sbert.net/)
* [Streamlit](https://docs.streamlit.io/)

---

