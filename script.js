document.addEventListener('alpine:init', () => {
  Alpine.data('emailAnalyzer', () => ({
    emailText: '',
    isLoading: false,
    result: null,
    error: null,
    fileName: 'Nenhum arquivo selecionado',
    copyButtonText: 'Copiar',
    typingInterval: null,

    async submitForm() {
      this.isLoading = true;
      this.result = null;
      this.error = null;
      clearInterval(this.typingInterval);

      const fileInput = document.getElementById('fileInput');
      const file = fileInput && fileInput.files ? fileInput.files[0] : null;

      if (!this.emailText.trim() && !file) {
        this.error = 'Opa! Precisa mandar um texto ou um arquivo.';
        this.isLoading = false;
        return;
      }

      const formData = new FormData();
      if (this.emailText.trim()) {
        formData.append('texto', this.emailText);
        if (fileInput) {
          fileInput.value = '';
        }
        this.fileName = 'Nenhum arquivo selecionado';
      } else if (file) {
        formData.append('arquivo', file);
      }

      try {
        const response = await fetch('https://automatiza-o-de-e-mails-production.up.railway.app/analyze', {
          method: 'POST',
          body: formData
        });

        if (!response.ok) {
          // tenta ler JSON, mas se não tiver corpo, não quebra
          let errorData = {};
          try {
            errorData = await response.json();
          } catch (_) {
            // sem corpo JSON
          }
          const msg = errorData?.detail || `Erro ${response.status}: Deu ruim no servidor. Tenta de novo.`;
          throw new Error(msg);
        }

        // mesma proteção para corpo vazio
        let data = {};
        try {
          data = await response.json();
        } catch (_) {
          throw new Error('Resposta vazia do servidor.');
        }

        this.result = {
          classification: data.classificacao,
          suggestion: data.resposta_sugerida
        };

        this.typeWriterEffect(this.result.suggestion);
      } catch (err) {
        this.error = err?.message || 'Erro de conexão. O backend tá rodando?';
      } finally {
        this.isLoading = false;
      }
    },

    loadExample(type) {
      this.clearForm();
      const examples = {
        produtivo: 'Prezados, gostaria de saber o status atualizado do meu pedido nº 8451. Poderiam verificar se já foi enviado? Agradeço a atenção.',
        improdutivo: 'Olá equipe, passando para desejar a todos um excelente final de semana e um bom descanso! Abraços.'
      };
      this.emailText = examples[type] || '';
    },

    copySuggestion() {
      if (!this.result || !this.result.suggestion) {
        return;
      }
      navigator.clipboard.writeText(this.result.suggestion).then(() => {
        this.copyButtonText = 'Copiado!';
        setTimeout(() => {
          this.copyButtonText = 'Copiar';
        }, 2000);
      });
    },

    clearForm() {
      this.emailText = '';
      const fileInput = document.getElementById('fileInput');
      if (fileInput) {
        fileInput.value = '';
      }
      this.fileName = 'Nenhum arquivo selecionado';
      this.result = null;
      this.error = null;
      this.copyButtonText = 'Copiar';
      clearInterval(this.typingInterval);
      const suggestionEl = document.getElementById('suggestion-text');
      if (suggestionEl) {
        suggestionEl.innerHTML = '';
        suggestionEl.style.setProperty('--cursor-animation', 'none');
      }
    },

    typeWriterEffect(text) {
      const suggestionEl = document.getElementById('suggestion-text');
      if (!text || !suggestionEl) {
        return;
      }

      clearInterval(this.typingInterval);
      suggestionEl.innerHTML = '';

      let i = 0;
      const speed = 30;

      this.typingInterval = setInterval(() => {
        if (i < text.length) {
          suggestionEl.innerHTML += text.charAt(i);
          i += 1;
        } else {
          clearInterval(this.typingInterval);
          suggestionEl.style.setProperty('--cursor-animation', 'none');
        }
      }, speed);

      suggestionEl.style.setProperty('--cursor-animation', 'blink-cursor 1s step-end infinite');
    }
  }));
});
