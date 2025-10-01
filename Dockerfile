FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- LINHA ADICIONADA AQUI ---
# Este comando descarrega os pacotes do NLTK durante a construção da imagem
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('punkt_tab')"

COPY . .

ENV PYTHONUNBUFFERED=1
EXPOSE $PORT

CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}"]