# Decifrador de E-mails com IA 🤖

Aplicação web que utiliza a API do Google Gemini para classificar o conteúdo de e-mails em "Produtivo" ou "Improdutivo" e sugerir uma resposta automática. A interface permite a análise de texto colado ou o upload de arquivos `.txt`.

---

### Tecnologias Utilizadas

* **Backend:** Python, FastAPI, Uvicorn, Google Generative AI (Gemini), NLTK
* **Frontend:** HTML, CSS, JavaScript, Alpine.js

---

### Como Instalar e Rodar o Projeto

#### **Instruções**

1.  **Clone** o repositório e **entre** na pasta do projeto.
2.  **Crie e ative** o ambiente virtual para isolar as dependências.
3.  **Instale** todas as bibliotecas necessárias com um único comando.
4.  **Configure sua chave de API** criando um arquivo `.env` (instrução manual abaixo).
5.  **Execute** a aplicação (iniciando o backend e o frontend em terminais separados).

#### **Comandos para Instalação**

Copie e cole os comandos abaixo no seu terminal. Eles correspondem aos passos 1, 2 e 3 das instruções.

```bash
# Passo 1: Clonar e entrar na pasta
git clone <URL_DO_SEU_REPOSITORIO_GIT>
cd <NOME_DA_PASTA_DO_PROJETO>

# Passo 2: Criar e ativar o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Passo 3: Instalar dependências
pip install -r requirements.txt
Atenção Windows: Para ativar o ambiente virtual (parte do Passo 2), o comando é .venv\Scripts\activate.

Configuração Manual
Chave de API (Passo 4)
Crie um arquivo chamado .env na raiz do projeto e adicione sua chave da API do Gemini.

GEMINI_API_KEY=SUA_CHAVE_SECRETA_VAI_AQUI
Executando a Aplicação (Passo 5)
Você precisará de dois terminais abertos na pasta do projeto (e com o ambiente virtual ativado).

1. Backend
Em um terminal, inicie o servidor da API.

Bash

uvicorn api:app --reload
Deixe este terminal rodando. O backend estará disponível em http://127.0.0.1:8000.

2. Frontend
A forma mais fácil é usar a extensão Live Server no VS Code.

Clique com o botão direito no arquivo index.html.

Selecione "Open with Live Server".

O frontend abrirá no seu navegador, geralmente em http://1.2.3.4:5500.