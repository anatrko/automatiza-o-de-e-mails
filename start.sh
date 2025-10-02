#!/bin/bash

echo "--- INICIANDO O SCRIPT start.sh ---"

# Move para o diretório de trabalho, se necessário (boa prática)
cd /app

echo "--- A TENTAR INICIAR O SERVIDOR UVICORN... ---"

# Executa o servidor
uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}

echo "--- O COMANDO UVICORN TERMINOU (ISTO INDICA UMA FALHA) ---"