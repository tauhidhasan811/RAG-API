import os
from huggingface_hub import InferenceClient


API_TOKEN = os.environ["HF_TOKEN"] 


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"D:\RAG-API\rag-api\gemeni_api.json"


gemini_model = "models/text-embedding-004"
gpt_model = "openai/gpt-oss-120b"
def client():
    API_TOKEN = os.environ["HF_TOKEN"]
    client = InferenceClient(api_key=API_TOKEN, provider="novita")
    return client