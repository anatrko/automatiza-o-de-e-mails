document.addEventListener('alpine:init', () => {
    
    Alpine.data('emailAnalyzer', () => ({
        
        emailText: '',
        isLoading: false,
        result: null,
        error: null,
        fileName: 'Nenhum arquivo selecionado',
        copyButtonText: 'Copiar',
        
        // NOVO: Variável para controlar a animação de digitação
        typingInterval: null,

        // ... (as outras funções como submitForm, loadExample, etc. continuam aqui)
        async submitForm() {
            this.isLoading = true;
            this.result = null;
            this.error = null;
            clearInterval(this.typingInterval); // Limpa animação anterior

            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];
            
            if (!this.emailText.trim() && !file) {
                this.error = 'Opa! Precisa mandar um texto ou um arquivo.';
                this.isLoading = false; return;
            }

            const formData = new FormData();
            if (this.emailText.trim()) {
                formData.append('texto', this.emailText);
                fileInput.value = ''; this.fileName = 'Nenhum arquivo selecionado';
            } else {
                formData.append('arquivo', file);
            }

            try {
                const response = await fetch('https://automatiza-o-de-e-mails-production.up.railway.app/analyze/', {
                    method: 'POST', body: formData,
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || 'Deu ruim no servidor. Tenta de novo.');
                }

                const data = await response.json();
                
                this.result = {
                    classification: data.classificacao,
                    suggestion: data.resposta_sugerida,
                };

            } catch (err) {
                this.error = err.message || 'Erro de conexão. O backend tá rodando?';
            } finally {
                this.isLoading = false;
            }
        },

        loadExample(type) { /* ... sem alterações ... */
            this.clearForm();
            const examples = {
                produtivo: "Prezados, gostaria de saber o status atualizado do meu pedido nº 8451. Poderiam verificar se já foi enviado? Agradeço a atenção.",
                improdutivo: "Olá equipe, passando para desejar a todos um excelente final de semana e um bom descanso! Abraços."
            };
            this.emailText = examples[type];
        },
        copySuggestion() { /* ... sem alterações ... */
            if (!this.result?.suggestion) return;
            navigator.clipboard.writeText(this.result.suggestion).then(() => {
                this.copyButtonText = 'Copiado!';
                setTimeout(() => { this.copyButtonText = 'Copiar'; }, 2000);
            });
        },
        clearForm() { /* ... sem alterações ... */
            this.emailText = ''; document.getElementById('fileInput').value = '';
            this.fileName = 'Nenhum arquivo selecionado';
            this.result = null; this.error = null; this.copyButtonText = 'Copiar';
            clearInterval(this.typingInterval);
            const suggestionEl = document.getElementById('suggestion-text');
            if (suggestionEl) suggestionEl.innerHTML = '';
        },

        // --- NOVA FUNÇÃO PARA O EFEITO MÁQUINA DE ESCREVER ---
        typeWriterEffect(text) {
            const suggestionEl = document.getElementById('suggestion-text');
            if (!text || !suggestionEl) return;

            // Limpa qualquer animação anterior e o texto
            clearInterval(this.typingInterval);
            suggestionEl.innerHTML = '';
            
            let i = 0;
            const speed = 30; // Velocidade em milissegundos

            this.typingInterval = setInterval(() => {
                if (i < text.length) {
                    suggestionEl.innerHTML += text.charAt(i);
                    i++;
                } else {
                    clearInterval(this.typingInterval);
                    // Opcional: esconder o cursor quando terminar
                    suggestionEl.style.setProperty('--cursor-animation', 'none');
                }
            }, speed);

            // Garante que o cursor pisque desde o início
            suggestionEl.style.setProperty('--cursor-animation', 'blink-cursor 1s step-end infinite');
        }
    }));
});
