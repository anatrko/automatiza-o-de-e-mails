// Ouve o evento de 'submit' do formulário
document.getElementById('emailForm').addEventListener('submit', async (e) => {
    e.preventDefault(); // Impede o envio padrão do formulário (recarregar a página)

    const API_URL = 'http://127.0.0.1:8000/analyze/'; // Use o endpoint que aceita arquivo/texto
    
    const texto = document.getElementById('emailTexto').value.trim();
    const arquivo = document.getElementById('emailFile').files[0]; // Pega o arquivo
    
    const loading = document.getElementById('loading');
    const resultadoDiv = document.getElementById('resultado');
    const categoriaP = document.getElementById('categoria');
    const respostaP = document.getElementById('resposta');

    if (!texto && !arquivo) {
        alert("Digite o email OU selecione um arquivo antes de enviar!");
        return;
    }

    // --- Lógica de Envio com FormData ---
    const formData = new FormData();
    
    // Anexa o campo de texto, mesmo que esteja vazio (FastAPI precisa dele)
    formData.append('texto', texto); 
    
    if (arquivo) {
        // 'arquivo' deve ser o mesmo nome do parâmetro no seu endpoint do FastAPI:
        // async def analyze_email_document(..., arquivo: UploadFile = File(None))
        formData.append('arquivo', arquivo); 
    }

    loading.classList.remove('hidden');
    resultadoDiv.classList.add('hidden');
    categoriaP.textContent = '';
    respostaP.textContent = '';

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            // Ao usar FormData, NÃO defina o header 'Content-Type', o browser faz isso corretamente
            // headers: { 'Content-Type': 'application/json' } <-- REMOVIDO!
            body: formData
        });

        if (!response.ok) {
             // Tenta pegar a mensagem de erro do FastAPI (se houver)
            const errorData = await response.json().catch(() => ({ detail: "Erro desconhecido" }));
            throw new Error(`Erro ${response.status}: ${errorData.detail || 'Falha na comunicação com a API.'}`);
        }

        const data = await response.json();
        
        // --- Lógica de Exibição (aprimorada para destacar a categoria) ---
        categoriaP.textContent = data.categoria;
        respostaP.textContent = data.resposta;
        
        // Adiciona classes para estilo dinâmico
        categoriaP.className = data.categoria === 'Produtivo' ? 'produtivo-text' : 'improdutivo-text';

        resultadoDiv.classList.remove('hidden');
    } catch (error) {
        alert(error.message);
    } finally {
        loading.classList.add('hidden');
    }
});