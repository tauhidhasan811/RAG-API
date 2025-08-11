import math
from backend.services.reader import read_pdf, read_csv, read_docx,read_text, read_image, read_sql


def create_chunk(file_path ,chunk_size=300):

    meta_data=[]
    chunk_text=[]
    file_type = file_path.split('.')[-1]
    if file_type == 'pdf':
        text = read_pdf(file_path)
    elif file_type == 'txt':
        text = read_text(file_path)
    elif file_type == 'csv':
        text = read_csv(file_path)
    elif file_type == 'docx':
        text = read_docx(file_path) 
    elif file_type in ['jpg', 'jpeg', 'png']:
        text = read_image(file_path)
    elif file_type == 'db':
        text = read_sql(file_path)
    else:
        return chunk_text,meta_data 
    if text == 'nodata':
        return ['nodata'], ['nodata']

    idx = 0
    word_count = 0
    current_chunk=""
    text = text.split('.')
    filename = file_path.split('/')[-1].split('.')[0]
    i = 0
    for sentence in text:
        #print(sentence)
        if word_count >= chunk_size:
            i +=1
            chunk_text.append(current_chunk)
            len_chunk = 0
            meta_data.append({
                "chunk_index": idx+len_chunk,
                "text": current_chunk,
                "embedding_id": idx + len_chunk,
                "filename": filename,
                "file_type": file_type
                })
            current_chunk=""
            word_count=0
            idx+=1
        word_count += len(sentence.split())
        current_chunk += sentence+'. '  
    if i ==0:
          chunk_text = [current_chunk]
          meta_data.append({
                "chunk_index": 0,
                "text": current_chunk,
                "embedding_id": 0,
                "filename": filename,
                "file_type": file_type
                })
    return chunk_text, meta_data
