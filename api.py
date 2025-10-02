import os
import json
import traceback
from dotenv import load_dotenv
from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# --- Inicialização do app ---
app = FastAPI(title="Análise de E-mail com Gemini API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Configuração do Gemini ---
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
if not gemini_key:
    raise ValueError("A chave GEMINI_API_KEY não foi encontrada.")

genai.configure(api_key=gemini_key)
GEMINI_MODEL = "gemini-pro-latest"

# --- Rotas ---
@app.get("/", summary="Verificação de status", tags=["Geral"])
def read_root():
    return {"status": "ok", "message": "O backend está a funcionar!"}

@app.post("/analyze", summary="Analisa email ou documento", tags=["Análise de Email"])
async def analyze_email_document(
    texto: str = Form(None, description="Conteúdo do email digitado diretamente."),
    arquivo: UploadFile = File(None, description="Arquivo de email (.txt).")
):
    email_content = ""
    if texto and texto.strip():
        email_content = texto
    elif arquivo:
        if arquivo.content_type != "text/plain":
            raise HTTPException(status_code=400, detail="Formato de arquivo não suportado. Use apenas .txt.")
        try:
            content_bytes = await arquivo.read()
            email_content = content_bytes.decode('utf-8', errors='ignore')
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao ler arquivo: {e}")

    if not email_content.strip():
        raise HTTPException(status_code=400, detail="É necessário fornecer texto válido ou um arquivo com conteúdo.")

    # Apenas uma limpeza básica, sem NLTK
    content_for_ia = email_content.lower().strip()

    try:
        system_instruction = "Você é um assistente de triagem de e-mails..."

        model = genai.GenerativeModel(GEMINI_MODEL, system_instruction=system_instruction)

        prompt = f"""
        Analise o conteúdo do e-mail abaixo e classifique-o estritamente como 'Produtivo' ou 'Improdutivo'.
        Gere também uma resposta sugerida apropriada.
        **Formato de Saída Obrigatório:** JSON com "classificacao" e "resposta_sugerida".
        ---
        {content_for_ia}
        ---
        """

        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(response_mime_type="json", temperature=0.0),
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
            }
        )
        
        try:
            ia_result = json.loads(response.text)
        except json.JSONDecodeError as e:
            return {"status": "erro", "message": "Resposta da IA em formato inválido"}

        return {
            "status": "sucesso",
            "classificacao": ia_result.get("classificacao", "Improdutivo"),
            "resposta_sugerida": ia_result.get("resposta_sugerida", "Não foi possível gerar uma resposta.")
        }

    except Exception as e:
        print(f"ERRO GENÉRICO NO BACKEND: {type(e).__name__} - {str(e)} - Traceback: {''.join(traceback.format_exception(type(e), e, e.__traceback__))}")
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {str(e)}")