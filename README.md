Absolutely! Here’s the **How to Run** section formatted for your `README.md` file on GitHub:

````markdown
# How to Run the RAG API

## 1. Running Locally (Without Docker)

### Step 1: Clone the repository
```bash
git clone https://github.com/your-org/rag-api.git
cd rag-api
````

### Step 2: Create and activate a Python virtual environment

```bash
python -m venv venv
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Setup environment variables

Create a `.env` file in the project root with your API keys and config, for example:

```env
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
HUGGINGFACE_API_KEY=your_huggingface_key
GPT_MODEL=gpt-oss-120b
GEMINI_MODEL=gemini-1.5-flash
VECTOR_DB_PATH=storage/vector_store
METADATA_PATH=storage/metadata
```

### Step 5: Run the FastAPI backend server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

* Access the API at: [http://localhost:8000](http://localhost:8000)
* Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### Step 6 (optional): Run frontend (if applicable)

If using Streamlit or another frontend, navigate to its folder and run:

```bash
streamlit run frontend_app.py
```

* Access the frontend UI at [http://localhost:8501](http://localhost:8501)

---

## 2. Running with Docker

### Step 1: Build Docker images

```bash
docker-compose build
```

### Step 2: Create a `.env` file in the root folder (same format as above)

### Step 3: Start Docker containers

```bash
docker-compose up
```

* Backend will run on port `8000`
* Frontend will run on port `8501`

### Step 4: Access the app

* API: [http://localhost:8000](http://localhost:8000)
* Frontend: [http://localhost:8501](http://localhost:8501)

---

## Troubleshooting

* Ensure Docker Desktop is running before executing Docker commands.
* Confirm your `.env` file contains all required API keys.
* Verify ports 8000 and 8501 are not blocked or used by other processes.
* Use `docker-compose logs` to inspect container logs for errors.

---

If you need help with sample `.env` or testing examples, feel free to ask!

```

Let me know if you want me to help integrate this into your full README!
```
