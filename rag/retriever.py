import os
import faiss
from backend.services.reader import read_metaData
from pandas.errors import EmptyDataError


def get_related_chunk(query_embedding, model_name, threshold=1.5):
    faiss_root = f'backend/storage/{model_name}/faiss'
    metaData_root = f'backend/storage/{model_name}/metadata'
    faissdir = [os.path.join(faiss_root, path) for path in os.listdir(faiss_root)]
    metadatdir = [os.path.join(metaData_root, path) for path in os.listdir(metaData_root)]
    relevant_chunks = []

    for i in range(len(metadatdir)):
        me_file = metadatdir[i].split('\\')[-1].split('.')[0]
        da_file = faissdir[i].split('\\')[-1].split('.')[0]
        if me_file == da_file:
            faiss_index = faiss.read_index(faissdir[i])
            try:
                text_chunks = read_metaData(metadatdir[i])
                distances, indices = faiss_index.search(query_embedding, k=3)

                filtered_indices = [idx for dist, idx in zip(distances[0], indices[0]) if idx != -1 and dist <= threshold]

                if len(filtered_indices) <= 1:
                    chunks = [text_chunks[i][0]['text'] for i in filtered_indices]
                else:
                    chunks = [text_chunks[0][i]['text'] for i in filtered_indices]

                relevant_chunks.extend(chunks)

            except EmptyDataError:
                continue

    relevant_chunks = [text.strip() for text in relevant_chunks]
    relevant_chunks = "\n\n".join(relevant_chunks)

    return relevant_chunks
