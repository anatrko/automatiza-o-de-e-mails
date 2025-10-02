# Leitor de E-mails com IA

Aplicação web que utiliza a API do Google Gemini para classificar o conteúdo de e-mails em "Produtivo" ou "Improdutivo" e sugerir uma resposta automática. A interface permite a análise de texto colado ou o upload de arquivos `.txt`.

---

### Tecnologias Utilizadas

* **Backend:**
    * Python
    * FastAPI
    * Uvicorn
    * Google Generative AI (Gemini)

* **Frontend:**
    * HTML
    * CSS
    * JavaScript
    * Alpine.js

---

### Como Instalar e Rodar o Projeto

Siga os passos abaixo para configurar e executar a aplicação em sua máquina local.

**1. Clone o Repositório**

Primeiro, use o comando `git clone` para baixar os arquivos do projeto.

```bash
git clone <URL_DO_SEU_REPOSITORIO_GIT>
```
Depois, entre na pasta que foi criada.

```Bash

cd <NOME_DA_PASTA_DO_PROJETO>
Nota: Para atualizar um projeto que já existe, entre na pasta e use o comando git pull.
```

2. Crie e Ative o Ambiente Virtual

Para não misturar as bibliotecas do projeto com as do seu sistema, crie um ambiente virtual.

```Bash

python3 -m venv .venv
```
Agora, ative este ambiente. Escolha o comando certo para o seu sistema:

Para Windows:

```Bash

.venv\Scripts\activate
```
Para macOS ou Linux:

```Bash

source .venv/bin/activate
```
3. Instale as Dependências

O arquivo requirements.txt já está no projeto. Use o comando abaixo para instalar tudo o que é necessário.

```Bash

pip install -r requirements.txt
```
4. Configure a Chave de API

Este passo é manual. Crie um arquivo chamado .env na pasta principal e adicione sua chave da API do Gemini, como no exemplo abaixo.

GEMINI_API_KEY=SUA_CHAVE_SECRETA_VAI_AQUI
5. Execute a Aplicação

Você precisará de dois terminais abertos na pasta do projeto (ambos com o ambiente virtual ativado).

Inicie o Backend
Em um terminal, execute o comando abaixo para ligar a API.

```Bash 

uvicorn api:app --reload 
```
Deixe este terminal aberto. A API estará rodando em http://127.0.0.1:8000.

Inicie o Frontend
A forma mais simples é usando a extensão Live Server no VS Code.

Clique com o botão direito no arquivo index.html.

Selecione "Open with Live Server".

A interface web abrirá no seu navegador, geralmente em http://127.0.0.1:5500.