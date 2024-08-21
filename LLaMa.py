import requests
from dotenv import load_dotenv
import os

load_dotenv()
async def response_gen(context:str, query:str):


    api_url = "https://api-inference.huggingface.co/models/bert-large-uncased-whole-word-masking-finetuned-squad"
    api_key = os.environ.get("HF_TOKEN")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }



    data = {
        "inputs": {
            "question": query,
            "context": context
        }
    }


    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["answer"]
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
