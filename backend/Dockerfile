
#FROM python:3.10

#WORKDIR /app

#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt

#COPY . .

#CMD ["uvicorn", "fast_api_with_gpt:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpoppler-cpp-dev \
    pkg-config \
    poppler-utils \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

COPY noted-flash-459002-k8-bf0ac08c5bb8.json /app/credentials.json

ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
