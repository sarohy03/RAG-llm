from bs4 import BeautifulSoup
import requests
import re

def fetch_website_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()


def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'(?<=[.,!?])(?=[^\s])', r' ', text)
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)

    return text


def rag_system(url: str):
    content = fetch_website_content(url)
    preprocessed_content = preprocess_text(content)

    return preprocessed_content



