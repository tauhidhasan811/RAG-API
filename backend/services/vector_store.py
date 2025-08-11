#import os
import faiss
import numpy as np
from rag.embedding_utils import data_embedding, image_embedding

     
def create_faiss_index_and_map(text_chunks, model_name):
    if not text_chunks:
        return None, None

    print("Creating embeddings for text chunks...")
    embeddings = []
    for chunk in text_chunks:
        if model_name == "Gemini":
            embedding=data_embedding(chunk=chunk,model_name=model_name)
        elif model_name == "GPT":
            embedding=data_embedding(chunk=chunk,model_name=model_name)
        else:
            return ""
        embeddings.append(embedding)

    embeddings_np = np.array(embeddings, dtype='float32')
    dimension = embeddings_np.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_np)

    print("FAISS index created with", len(embeddings), "embeddings.")

    return index



def create_faiss_index_and_map_for_images(images_data):

    if not images_data:
        print("No image data provided.")
        return None, None

    print("Creating embeddings for images...")
    embeddings = []
    
    for image_item in images_data:
        embedding = image_embedding(image_item)
        
        if embedding:
            embeddings.append(embedding)

    if not embeddings:
        print("No embeddings were successfully created.")
        return None, None
        
    # Convert embeddings to a numpy array for FAISS
    embeddings_np = np.array(embeddings, dtype='float32')
    dimension = embeddings_np.shape[1]


    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_np)

    print("FAISS index created with", len(embeddings), "embeddings.")

    return index, images_data
