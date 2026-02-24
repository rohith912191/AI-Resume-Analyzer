FROM python:3.8-slim

WORKDIR /app

# Install system dependencies required for spacy build
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "App/App.py", "--server.port=8501", "--server.address=0.0.0.0"]