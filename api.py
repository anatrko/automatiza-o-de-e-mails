import os
import json
import nltk
from dotenv import load_dotenv
from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# --- 1. Configuração do Gemini ---
# <<< ALTERAÇÃO AQUI: A importação agora é do 'google.generativeai'
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Carrega variáveis de ambiente (necessário para GEMINI_API_KEY)
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

if not gemini_key:
    # Se a chave não for encontrada, o script falha aqui com uma mensagem clara
    raise ValueError("A chave GEMINI_API_KEY não foi encontrada no ambiente ou no arquivo .env.")

# <<< ALTERAÇÃO AQUI: A configuração é feita com genai.configure()
genai.configure(api_key=gemini_key)

# <<< ALTERAÇÃO AQUI: Nome do modelo corrigido para um modelo válido e atual
GEMINI_MODEL = "gemini-pro-latest"

# --- 2. Configuração do NLTK (Garante que os recursos estão baixados) ---

def setup_nltk():
    """Garante que os recursos do NLTK estão baixados capturando LookupError."""
    resources = ['stopwords', 'punkt'] # 'punkt_tab' geralmente não é necessário
    
    for resource in resources:
        try:
            if resource == 'stopwords':
                nltk.data.find(f'corpora/{resource}')
            else:
                nltk.data.find(f'tokenizers/{resource}')
        except LookupError:
            print(f"Recurso NLTK '{resource}' não encontrado. Baixando...")
            nltk.download(resource, quiet=True) # Adicionado 'quiet=True' para uma saída mais limpa

# Chama a função para configurar o NLTK no início da API
setup_nltk()

# Define o conjunto de stop words em português
STOP_WORDS_PT = set(stopwords.words('portuguese'))

# --- 3. Funções de Pré-processamento ---

def preprocess_text(text: str) -> str:
    """Tokeniza, remove stop words, pontuação e retorna o texto limpo."""
    if not text:
        return ""
    
    text = text.lower().strip()
    tokens = word_tokenize(text, language='portuguese')
    
    clean_tokens = [
        word for word in tokens 
        if word.isalnum() and word not in STOP_WORDS_PT
    ]
    
    return " ".join(clean_tokens)

# --- 4. Configuração do FastAPI ---

app = FastAPI(
    title="Análise de E-mail com Gemini API",
    description="API para classificar o conteúdo de e-mails e sugerir respostas usando IA Generativa."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 5. Endpoints da API ---

@app.get("/", summary="Verificação de status", tags=["Geral"])
def read_root():
    return {"status": "ok", "message": "O backend de análise de e-mail está funcionando!"}


@app.post("/analyze/", summary="Analisa email ou documento", tags=["Análise de Email"])
async def analyze_email_document(
    texto: str = Form(None, description="Conteúdo do email digitado diretamente."),
    arquivo: UploadFile = File(None, description="Arquivo de email (.txt) via upload.")
):
    email_content = ""
    
    # 5.1. Lógica de Leitura de Conteúdo
    if texto and texto.strip():
        email_content = texto.strip()
    elif arquivo:
        try:
            content_bytes = await arquivo.read()
            email_content = content_bytes.decode('utf-8', errors='ignore')
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao ler arquivo: {e}")
    
    # 5.2. Validação
    if not email_content.strip():
        raise HTTPException(
            status_code=400, 
            detail="É necessário fornecer texto válido ou um arquivo com conteúdo."
        )

    # 5.3. Pré-processamento do Texto
    processed_content = preprocess_text(email_content)
    if not processed_content:
        # Se após o pré-processamento não sobrar nada (ex: só stopwords), retorne um erro.
        raise HTTPException(status_code=400, detail="O texto fornecido não contém conteúdo analisável.")

    # --- 5.4. Chamada à IA (Gemini) ---
    try:
        # <<< ALTERAÇÃO AQUI: A forma de chamar a API foi completamente reestruturada
        
        # 1. Instancia o modelo
        model = genai.GenerativeModel(
            GEMINI_MODEL,
            # A instrução de sistema é passada aqui
            system_instruction=(
                "Você é um classificador de e-mails de suporte automatizado e um assistente de resposta. "
                "Sua tarefa é analisar o conteúdo do email fornecido, classificá-lo e gerar uma resposta. "
                "Sua saída DEVE ser um objeto JSON válido com as chaves 'classificacao' e 'resposta_sugerida'."
            )
        )

        # 2. Define o prompt que será enviado ao modelo
        prompt = f"""
        Analise o seguinte conteúdo de e-mail e retorne um JSON com a classificação e uma sugestão de resposta.
        
        As categorias de classificação permitidas são: 'Status', 'Reclamação', 'Técnico', 'Outro'.
        A resposta sugerida deve ser profissional e ter entre 2 e 3 frases.

        Conteúdo do E-mail:
        ---
        {processed_content}
        ---
        """
        
        # 3. Faz a Chamada à Gemini API, configurando para retornar JSON
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json", # Pede a saída em JSON
                temperature=0.1 # Temperatura baixa para respostas mais consistentes
            ),
            # Medida de segurança para evitar bloqueios por conteúdo sensível
            safety_settings={
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
        )
        
        # 4. Processa a resposta
        ia_result = json.loads(response.text)

        return {
            "status": "sucesso",
            "classificacao": ia_result.get("classificacao", "Não Classificado"),
            "resposta_sugerida": ia_result.get("resposta_sugerida", "Não foi possível gerar uma resposta.")
        }

    # --- 5.5. Tratamento de Erro ---
    except json.JSONDecodeError:
        print(f"ERRO: Gemini não retornou JSON válido: {response.text}")
        raise HTTPException(
            status_code=500, 
            detail="Erro ao decodificar a resposta JSON do Gemini. O modelo pode ter retornado um formato inesperado."
        )
    except Exception as e:
        print(f"ERRO GENÉRICO NO BACKEND: {type(e).__name__} - {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {e}")