FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r App/requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "App/App.py", "--server.port=8501", "--server.address=0.0.0.0"]
