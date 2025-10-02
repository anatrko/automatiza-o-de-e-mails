FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- LINHA CRUCIAL ADICIONADA AQUI ---
# Descarrega os pacotes do NLTK durante a construção, para uma pasta padrão
RUN python -c "import nltk; nltk.download(['stopwords', 'punkt', 'punkt_tab'])"

COPY . .

# Removemos o CMD para usar o Procfile, que é mais explícito
# CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}"]