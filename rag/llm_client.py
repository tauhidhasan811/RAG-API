import os
import numpy as np
from huggingface_hub import InferenceClient
from rag.embedding_utils import data_embedding
from rag.retriever import get_related_chunk
import google.generativeai as genai

#def response_rag(query, faiss_index, text_chunks, model_name, image_data=None, k=3):
def response_rag(query, model_name, image_data=None, k=3):
    if len(os.listdir(f'backend/storage/{model_name}/faiss')) == 0:
        return "No document index available. Please process a document first."

    query_embedding = None

    if model_name == 'Gemini':
        if image_data is not None and query:
            # Get separate embeddings for text and image
            text_emb = genai.embed_content(
                model="models/text-embedding-004",
                content=query
            )['embedding']
            image_emb = genai.embed_content(
                model="models/text-embedding-004",
                content=image_data
            )['embedding']

            # Average the two embeddings (simple fusion)
            query_embedding = np.mean([text_emb, image_emb], axis=0).astype('float32')

        elif image_data is not None:
            # Image only embedding
            query_embedding = np.array(
                [genai.embed_content(model="models/text-embedding-004", content=image_data)['embedding']],
                dtype='float32'
            )

        else:
            # Text only embedding
            query_embedding = np.array(
                [data_embedding(query, model_name)],
                dtype='float32'
            )

    elif model_name == 'GPT':
        # GPT embedding (text only)
        query_embedding = data_embedding([query], model_name)


    relevant_chunks = get_related_chunk(query_embedding, model_name)
    # Prepare prompt and generate answer
    if model_name == 'Gemini':
        prompt_context = "\n\n".join(relevant_chunks)
        final_prompt = (
            f"Consider you are a chat bot. Using the following context, answer the user's question. "
            f"Always respond in one paragraph.\n\nContext:\n{prompt_context}\n\nQuestion: {query}"
        )
        messages = [{"role": "user", "parts": [{"text": final_prompt}]}]
        generation_model = genai.GenerativeModel('gemini-1.5-flash')
        response = generation_model.generate_content(messages).text

    elif model_name == "GPT":
        context = "\n---\n".join(relevant_chunks)
        prompt = f"Context:\n{context}\n\nQuestion: {query}"
        API_TOKEN = os.environ.get("HF_TOKEN")
        client = InferenceClient(api_key=API_TOKEN, provider="novita")
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."
                " If you do not find any related chunk with the user question say sorry that you can not anser."
                " if find Always respond with a single paragraph of plain text. Do not use tables, bullet points, or markdown."},
                {"role": "user", "content": prompt},
            ],
        )
        response = completion.choices[0].message["content"]

    return response
