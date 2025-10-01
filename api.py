import os
import json
import nltk
import traceback  # Adicionado para debug
from dotenv import load_dotenv
from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from fastapi.staticfiles import StaticFiles

# A biblioteca Pillow não é mais necessária
# from PIL import Image 
# A biblioteca io não é mais necessária
# import io 
app = FastAPI()
app.mount("/", StaticFiles(directory=".", html=True), name="static")

load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

if not gemini_key:
    raise ValueError("A chave GEMINI_API_KEY não foi encontrada no ambiente ou no arquivo .env.")

genai.configure(api_key=gemini_key)

# <<< VOLTANDO PARA O MODELO DE TEXTO QUE FUNCIONA NA SUA CONTA
GEMINI_MODEL = "gemini-pro-latest"

def setup_nltk():
    resources = ['stopwords', 'punkt']
    for resource in resources:
        try:
            nltk.data.find(f'corpora/{resource}' if resource == 'stopwords' else f'tokenizers/{resource}')
        except LookupError:
            nltk.download(resource, quiet=True)
setup_nltk()
STOP_WORDS_PT = set(stopwords.words('portuguese'))

def preprocess_text(text: str) -> str:
    if not text: return ""
    text = text.lower().strip()
    tokens = word_tokenize(text, language='portuguese')
    clean_tokens = [word for word in tokens if word.isalnum() and word not in STOP_WORDS_PT]
    return " ".join(clean_tokens)

# Redefine app com o título e aplica o CORS imediatamente
app = FastAPI(title="Análise de E-mail com Gemini API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://automatiza-o-de-e-mails.vercel.app",  # URL exata do frontend na Vercel
        "*"  # Temporário para testes; remova em produção
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Remove a instância redundante de CORSMiddleware
# app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/", summary="Verificação de status", tags=["Geral"])
def read_root():
    return {"status": "ok", "message": "O backend de análise de e-mail está funcionando!"}

@app.post("/analyze/", summary="Analisa email ou documento", tags=["Análise de Email"])
async def analyze_email_document(
    texto: str = Form(None, description="Conteúdo do email digitado diretamente."),
    arquivo: UploadFile = File(None, description="Arquivo de email (.txt).")
):
    # <<< VOLTANDO PARA A LÓGICA SIMPLES DE TEXTO
    email_content = ""
    if texto and texto.strip():
        email_content = texto.strip()
    elif arquivo:
        if arquivo.content_type != "text/plain":
             raise HTTPException(status_code=400, detail=f"Formato de arquivo não suportado. Use apenas .txt.")
        try:
            content_bytes = await arquivo.read()
            email_content = content_bytes.decode('utf-8', errors='ignore')
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao ler arquivo: {e}")
    
    if not email_content.strip():
        raise HTTPException(status_code=400, detail="É necessário fornecer texto válido ou um arquivo com conteúdo.")

    processed_content = preprocess_text(email_content)
    if not processed_content:
        raise HTTPException(status_code=400, detail="O texto fornecido não contém conteúdo analisável.")

    try:
        system_instruction = "Você é um assistente de triagem de e-mails..." # Mantém a mesma instrução de antes
        model = genai.GenerativeModel(GEMINI_MODEL, system_instruction=system_instruction)
        
        prompt = f"""
        Analise o conteúdo do e-mail abaixo e classifique-o estritamente como 'Produtivo' ou 'Improdutivo'.
        Gere também uma resposta sugerida apropriada.
        **Regras de Classificação...** (mantém as mesmas regras)
        **Formato de Saída Obrigatório:** JSON com "classificacao" e "resposta_sugerida".
        **Conteúdo do E-mail para Análise:**
        ---
        {processed_content} 
        ---
        """
        
        response = model.generate_content(
            prompt, # Enviando apenas o prompt de texto
            generation_config=genai.types.GenerationConfig(response_mime_type="application/json", temperature=0.0),
            safety_settings={ HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE, 
                             HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE, 
                             HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE, 
                             HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE }
        )
        
        # Trata possível erro no JSON da resposta
        try:
            ia_result = json.loads(response.text)
        except json.JSONDecodeError as e:
            print(f"ERRO AO DECODIFICAR JSON: {str(e)} - Resposta bruta: {response.text}")
            return {"status": "erro", "message": "Resposta da IA em formato inválido"}
        
        return {"status": "sucesso", "classificacao": ia_result.get("classificacao", "Improdutivo"), 
                "resposta_sugerida": ia_result.get("resposta_sugerida", "Não foi possível gerar uma resposta.")}
    except Exception as e:
        print(f"ERRO GENÉRICO NO BACKEND: {type(e).__name__} - {str(e)} - Traceback: {''.join(traceback.format_exception(type(e), e, e.__traceback__))}")
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")
