## ⚠️ Please read the documentation first

# Environment Setup

1. **Hugging Face API Key**  
   Go to **Windows Environment Variables → New**, set:  
   - Name: `HF_TOKEN`  
   - Value: `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`

2. **Gemini API Credentials**  
   Create a Google Cloud service account → download JSON key →  
   set its absolute path in `backend/core/config.py`:
   ```python
   os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:/RAG-API/rag-api/your-file.json"
> **Note:** An additional key will be provided via email.
3. **OCR Setup:**  
- To enable text extraction from images on Windows, set the default path for the Tesseract OCR executable in the file `backend/services/reader.py`.  
- The default path is usually: `C:\Program Files\Tesseract-OCR\tesseract.exe`.  
- Ensure Tesseract OCR is installed on your system; you can download it from [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).


# Start the Application

### Backend

```bash
pip install -r backend/requirements.txt
uvicorn backend.app.fast_api:app --reload
```

### Frontend

```bash
pip install -r frontend/requirements.txt
streamlit run frontend/app.py
```

> **Additional Note:** Still, this application works primarily via APIs, but some backend processes like finding related data and embedding user queries may take longer if you upload large or many documents. Using a GPU can improve performance for these tasks.
