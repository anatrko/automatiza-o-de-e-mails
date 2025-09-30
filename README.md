# Leitor de E-mails com IA

Aplicação web que utiliza a API do Google Gemini para classificar o conteúdo de e-mails em "Produtivo" ou "Improdutivo" e sugerir uma resposta automática. A interface permite a análise de texto colado ou o upload de arquivos `.txt`.
Obs: Projeto feito em ambiente Linux - WSL
---

### Tecnologias Utilizadas

* **Backend:**
    * Python
    * FastAPI
    * Uvicorn
    * Google Generative AI (Gemini)
    * NLTK

* **Frontend:**
    * HTML
    * CSS
    * JavaScript
    * Alpine.js

---

### Como Instalar e Rodar o Projeto

Siga os passos abaixo para configurar e executar a aplicação em sua máquina local.

**Pré-requisitos:**
* Git
* Python 3.8 ou superior

**1. Clone o Repositório**

Use o comando `git clone` para baixar os arquivos do projeto. Se você já tem o projeto e quer apenas atualizá-lo, use `git pull`.

```bash
# Para baixar pela primeira vez
git clone <URL_DO_SEU_REPOSITORIO_GIT>
cd <NOME_DA_PASTA_DO_PROJETO>

# Para atualizar um projeto existente
git pull origin main
2. Crie e Ative o Ambiente Virtual

Isso isola as dependências do projeto.

Bash

# Criar o ambiente
python3 -m venv .venv

# Ativar o ambiente
# No Windows:
.venv\Scripts\activate
# No macOS/Linux:
source .venv/bin/activate
3. Instale as Dependências

O arquivo requirements.txt já vem com o projeto. Com o ambiente virtual ativado, instale todas as bibliotecas com o seguinte comando:

Bash

pip install -r requirements.txt
4. Configure a Chave de API

Crie um arquivo chamado .env na raiz do projeto e adicione sua chave da API do Gemini.

GEMINI_API_KEY=SUA_CHAVE_SECRETA_VAI_AQUI
5. Execute a Aplicação

Você precisará de dois terminais abertos na pasta do projeto.

a) Inicie o Backend:
No primeiro terminal (com o ambiente .venv ativado), rode o servidor da API.

Bash

uvicorn api:app --reload
O backend estará disponível em http://127.0.0.1:8000.

b) Inicie o Frontend:
Se estiver usando o VS Code, a forma mais simples é com a extensão Live Server.

Clique com o botão direito no arquivo index.html.

Selecione "Open with Live Server".

O frontend abrirá no seu navegador, geralmente em http://127.0.0.1:5500.