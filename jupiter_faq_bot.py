from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from sentence_transformers import SentenceTransformer, util
import numpy as np
import google.generativeai as genai
import os
import streamlit as st
from dotenv import load_dotenv # Import load_dotenv

# Load environment variables from .env file
load_dotenv()

def scrape_faqs():
    # Setup driver
    service = Service("C:\\chromedriver-win64\\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)

    # Load the page
    driver.get("https://jupiter.money/contact/")
    time.sleep(5)

    # Scroll to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    # Get HTML after JS rendering
    html = driver.page_source
    driver.quit()

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all FAQ <li> blocks
    faq_list_items = soup.select('ul[data-controller="faq"] > li')

    data = []
    for item in faq_list_items:
        question_tag = item.find('button')
        answer_tag = item.find('p', attrs={"data-faq-target": True})

        if question_tag and answer_tag:
            question = question_tag.get_text(strip=True).replace('+', '').strip()
            answer = answer_tag.get_text(strip=True)
            data.append({'question': question, 'answer': answer})

    # Save as CSV
    df = pd.DataFrame(data)
    df.to_csv("jupiter_faqs.csv", index=False)
    print(f"✅ Scraped {len(df)} FAQs successfully.")
    return df

def preprocess_faqs(df):
    # Function to clean text
    def clean_text(text):
        if isinstance(text, str):
            clean = re.compile('<.*?>')
            text = re.sub(clean, '', text)
            text = ' '.join(text.split())
            # Add a space before 'or' if it's directly preceded by an email address
            text = re.sub(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})or', r'\1 or', text)
            # Add a space before 'at' if it's directly preceded by an email address
            text = re.sub(r'at([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', r'at \1', text)
        return text

    # Apply cleaning
    df['question'] = df['question'].apply(clean_text)
    df['answer'] = df['answer'].apply(clean_text)

    # Normalize questions
    def normalize_question(question):
        if isinstance(question, str):
            question = question.lower()
            question = re.sub(r'[^a-z0-9\s]', '', question)
        return question

    df['normalized_question'] = df['question'].apply(normalize_question)
    df.drop_duplicates(subset='normalized_question', keep='first', inplace=True)
    df.drop(columns=['normalized_question'], inplace=True)

    # Categorize content
    def categorize_faq(question, answer):
        question_lower = question.lower()
        answer_lower = answer.lower()

        if "kyc" in question_lower or "know your customer" in answer_lower:
            return "KYC"
        elif "card" in question_lower or "debit card" in answer_lower:
            return "Cards"
        elif "payment" in question_lower or "upi" in answer_lower:
            return "Payments"
        elif "account" in question_lower:
            return "Account Management"
        elif "rewards" in question_lower or "cashback" in answer_lower:
            return "Rewards"
        elif "loan" in question_lower or "credit" in question_lower:
            return "Loans/Credit"
        elif "support" in question_lower or "contact" in question_lower:
            return "Support/Contact"
        else:
            return "General"

    df['category'] = df.apply(lambda row: categorize_faq(row['question'], row['answer']), axis=1)
    df.to_csv("jupiter_faqs_preprocessed.csv", index=False)
    print(f"✅ Preprocessed and cleaned {len(df)} FAQs successfully.")
    return df

class FAQBot:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.df_faqs = pd.read_csv('jupiter_faqs_preprocessed.csv')
        self.df_faqs.columns = ['Question', 'Answer', 'Category']
        # Explicitly load the model to CPU
        self.model = SentenceTransformer('all-MiniLM-L12-v2') # Removed device='cpu'
        self.combined_texts = (self.df_faqs['Question'] + " " + self.df_faqs['Answer']).tolist()
        self.faq_embeddings = self.model.encode(self.combined_texts, convert_to_tensor=True)

    def rephrase_answer_with_llm(self, user_query, original_answer):
        try:
            model = genai.GenerativeModel('models/gemini-1.5-flash')  # Use the full model ID
            response = model.generate_content(
                f"User asked: '{user_query}'. Please respond in a simple, friendly, and natural tone. Answer: {original_answer}"
            )
            return response.text.strip()
        except Exception as e:
            print("LLM Error:", e)
            return original_answer  # fallback in case of error


    def get_faq_response(self, user_query, threshold=0.2):
        user_query_embedding = self.model.encode(user_query, convert_to_tensor=True)
        # cosine_scores = util.cos_sim(user_query_embedding, self.faq_answer_embeddings)[0]
        cosine_scores = util.cos_sim(user_query_embedding, self.faq_embeddings)[0]

        best_match_idx = np.argmax(cosine_scores).item()
        best_score = cosine_scores[best_match_idx].item()
    
        if best_score >= threshold:
            matched_question = self.df_faqs.loc[best_match_idx, 'Question']
            original_answer = self.df_faqs.loc[best_match_idx, 'Answer']
            category = self.df_faqs.loc[best_match_idx, 'Category']
            rephrased_answer = self.rephrase_answer_with_llm(user_query, original_answer)
    
            return {
                'status': 'confident',
                'question': matched_question,
                'answer': rephrased_answer,
                'category': category,
                'score': best_score
            }
        else:
            return {
                'status': 'unsure',
                'message': "I'm sorry, I couldn't find a relevant answer to your question. Could you please rephrase it or ask something else?"
            }

def main():
    st.set_page_config(page_title="Jupiter FAQ Bot", layout="wide")
    st.title("Jupiter FAQ Assistant")
    
    # Initialize bot
    # GEMINI_API_KEY = "------------------"  # Replace with your key
    # Retrieve API key from environment variables
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        st.error("GEMINI_API_KEY not found. Please set it in your .env file.")
        return

    bot = FAQBot(GEMINI_API_KEY)
    
    # Initialize session state for user_query if not already present
    if 'user_query' not in st.session_state:
        st.session_state.user_query = ""
    if 'exit_app' not in st.session_state:
        st.session_state.exit_app = False

    if not st.session_state.exit_app:
        user_input = st.text_input("Ask your question about Jupiter:", value=st.session_state.user_query, key="query_input")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit Query"):
                st.session_state.user_query = user_input
        with col2:
            if st.button("New Query"):
                st.session_state.user_query = ""
                st.rerun() # Changed from st.experimental_rerun()

        if st.session_state.user_query:
            response = bot.get_faq_response(st.session_state.user_query)
            
            if response['status'] == 'confident':
                st.success("Here's what I found:")
                st.markdown(f"**Matched Question:** {response['question']}")
                st.markdown(f"**Answer:** {response['answer']}")
                st.markdown(f"**Category:** {response['category']}")
                st.markdown(f"**Confidence Score:** {response['score']:.2f}")
            else:
                st.warning(response['message'])

        st.markdown("--- ")
        if st.button("Exit Application"):
            st.session_state.exit_app = True
            st.rerun() # Changed from st.experimental_rerun()
    else:
        st.info("Thank you for using the Jupiter FAQ Assistant. You can close this browser tab.")

if __name__ == "__main__":
    # Uncomment the following lines to scrape and preprocess FAQs
    faqs_df = scrape_faqs()
    preprocessed_df = preprocess_faqs(faqs_df)
    preprocessed_df.to_csv('jupiter_faqs_preprocessed.csv', index=False)
    print("FAQs scraped and preprocessed successfully!")
    # Run the Streamlit app
    main()
