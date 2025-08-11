
import os
import faiss
import tempfile
from pydantic import BaseModel
from rag.llm_client import response_rag
from backend.services.chunker import create_chunk
from backend.utils.file_utils import save_metadata
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from backend.services.vector_store import create_faiss_index_and_map


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

faiss_index = []
chunk_metadata = []
chunks_data = []

class QueryRequest(BaseModel):
    question: str

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    model_name: str = Query(...)
):
    global faiss_index, chunk_metadata, chunks_data

    ext = os.path.splitext(file.filename)[1].lower()

    if not ext:
        raise HTTPException(status_code=400, detail="Uploaded file has no extension.")
    
    allowed_exts = [".pdf", ".txt", ".csv", ".docx", ".jpg", ".jpeg", ".png", ".db"]
    if ext not in allowed_exts:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}. Allowed: {', '.join(allowed_exts)}"
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        contents = await file.read()
        tmp.write(contents)
        temp_path = tmp.name

    x=1
    chunks, metadata = create_chunk(temp_path)
    
    if  'nodata' not in chunks:
        index= create_faiss_index_and_map(text_chunks=chunks, 
                                            model_name=model_name)
        
        original_name = file.filename  
        name, ext = os.path.splitext(original_name)  
        ext_clean = ext[1:].lower()
        f_name = f"{name}_{ext_clean}_{model_name}"
        os.remove(temp_path)

        faiss_index = index
        if index != None:
            faiss.write_index(index, f"backend/storage/{model_name}/faiss/{f_name}.faiss")

        save_metadata(metadata=metadata, f_name=f_name, model_name=model_name)
        
        return {
            "message": f"{file.filename} uploaded and processed.",
            "chunks": len(chunks),
            "File name: ":(ext)
        }
    return {
        "message": f"{file.filename} uploaded and processed.",
        "chunks": "Data not saved",
        "File name: ":(ext),
        "chunk" : {chunks[0]}
    }

@app.post("/query")
async def query_doc(
    request: QueryRequest,
    model_name: str = Query(...)
):
    global faiss_index

    if faiss_index is None or chunk_metadata is None:
        raise HTTPException(status_code=400, detail="No PDF has been uploaded.")

    answer = response_rag(query=request.question,
                          model_name=model_name)
    
    return {"answer": answer}
class DeleteRequest(BaseModel):
    model_name: str

@app.post("/delete_files")
def delete_files(data: DeleteRequest):
    model_name = data.model_name
    faiss_root = f'backend/storage/{model_name}/faiss'
    metaData_root = f'backend/storage/{model_name}/metaData'

    def delete_files_in_dir(directory):
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)

    try:
        delete_files_in_dir(faiss_root)
        delete_files_in_dir(metaData_root)
        return {"detail": f"Files deleted for model '{model_name}'."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting files: {e}")

