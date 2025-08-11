from backend.core import config
import google.generativeai as genai
from sentence_transformers import SentenceTransformer

def data_embedding(chunk, model_name):
    if model_name=='Gemini':
        response = genai.embed_content( model=config.gemini_model, content=chunk )
        embedding = response['embedding']
        return embedding
    elif model_name =='GPT':
        embed_model = SentenceTransformer("all-MiniLM-L6-v2")
        embedding = embed_model.encode(chunk, convert_to_numpy=True)
        return embedding
    return None


def image_embedding(image_data):

    try:
        response = genai.embed_content(
            model=config.gemini_model, 
            content=[image_data]
        )
        return response['embedding']
    except Exception as e:
        print(f"Error creating image embedding: {e}")
        return None
