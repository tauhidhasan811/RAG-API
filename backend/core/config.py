import os
from huggingface_hub import InferenceClient


API_TOKEN = os.environ["HF_TOKEN"] # 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
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../noted-flash-459002-k8-bf0ac08c5bb8.json"
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:/RAG-API/rag-api/noted-flash-459002-k8-bf0ac08c5bb8.json"


gemini_model = "models/text-embedding-004"
gpt_model = "openai/gpt-oss-120b"
def client():
    API_TOKEN = os.environ["HF_TOKEN"]
    client = InferenceClient(api_key=API_TOKEN, provider="novita")
    return client