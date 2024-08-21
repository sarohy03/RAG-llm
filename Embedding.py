import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from Creating_Chunks import creating_chunks


def chunk_text(text, chunk_size=200):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


def vectorize_texts(texts):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(texts).toarray()
    return vectorizer, vectors


def find_relevant_content(query, texts):
    vectorizer, vectors = vectorize_texts(texts)
    query_vector = vectorizer.transform([query]).toarray().flatten()

    dot_products = np.dot(vectors, query_vector)

    most_relevant_index = np.argmax(dot_products)

    return texts[most_relevant_index]


def relevent_data(query: str, text: str):
    # Assuming `creating_chunks` chunks the text similar to `chunk_text`
    checked_text = creating_chunks(text)  # Ensure this returns a list of text chunks
    print(checked_text)

    # Find the most relevant content
    relevant_content = find_relevant_content(query, checked_text)

    return relevant_content