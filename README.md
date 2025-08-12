Here’s your environment setup and start instructions rewritten in a **clear, GitHub-friendly README.md format**:

````markdown
## Environment Setup

1. **Hugging Face API Key**  
   - Open `backend/core/config.py` and set your Hugging Face API key, or store it in environment variables for better security.  
   - To set it on Windows:  
     - Go to **Desktop → Edit Environment Variables → New**  
     - **Name:** `HF_TOKEN`  
     - **Value:** `your_access_token`  
       *(Example: `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`)*  

2. **Gemini API Credentials**  
   - You will receive a Google service account JSON file via email.  
   - Set the absolute path to this file in `backend/core/config.py`.  
     Example:  
     ```python
     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:/RAG-API/rag-api/noted-flash-459002-k8-bf0ac08c5bb8.json"
     ```

---

## Start the Application

### 1. Backend  
```bash
pip install -r backend/requirements.txt
uvicorn backend.app.fast_api:app --reload
````

### 2. Frontend

```bash
pip install -r frontend/requirements.txt
streamlit run frontend/app.py
```

```

If you want, I can **add a "Quick Start" section** on top so new developers can set it up in under 2 minutes. That’s very common in industrial README files.
```
