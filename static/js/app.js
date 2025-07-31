class GeminiChatApp {
    constructor() {
        this.isLoading = false;
        this.initializeElements();
        this.bindEvents();
        this.loadHistory();
    }

    initializeElements() {
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.modelInfoBtn = document.getElementById('modelInfoBtn');
        this.loadingIndicator = document.getElementById('loadingIndicator');
        this.charCount = document.querySelector('.char-count');
        this.modelModal = document.getElementById('modelModal');
        this.toastContainer = document.getElementById('toastContainer');
    }

    bindEvents() {
        // Send message events
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Auto-resize textarea
        this.messageInput.addEventListener('input', () => {
            this.updateCharCount();
            this.autoResizeTextarea();
        });

        // Clear chat
        this.clearBtn.addEventListener('click', () => this.clearChat());

        // Model info
        this.modelInfoBtn.addEventListener('click', () => this.showModelInfo());

        // Modal events
        this.modelModal.addEventListener('click', (e) => {
            if (e.target === this.modelModal || e.target.classList.contains('modal-close')) {
                this.closeModal();
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
            }
        });
    }

    autoResizeTextarea() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 120) + 'px';
    }

    updateCharCount() {
        const length = this.messageInput.value.length;
        this.charCount.textContent = `${length}/4000`;
        
        if (length > 3800) {
            this.charCount.style.color = 'var(--danger-color)';
        } else if (length > 3500) {
            this.charCount.style.color = 'var(--warning-color)';
        } else {
            this.charCount.style.color = 'var(--text-secondary)';
        }
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isLoading) return;

        // Add user message to chat
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.updateCharCount();
        this.autoResizeTextarea();

        // Show loading
        this.setLoading(true);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });

            const data = await response.json();

            if (response.ok) {
                this.addMessage(data.response, 'assistant');
            } else {
                throw new Error(data.error || 'Failed to send message');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            this.showToast('Error: ' + error.message, 'error');
            this.addMessage('Maaf, terjadi kesalahan. Silakan coba lagi.', 'assistant');
        } finally {
            this.setLoading(false);
        }
    }

    addMessage(content, role) {
        // Remove welcome message if it exists
        const welcomeMessage = this.chatMessages.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = role === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        // Format message content (basic markdown support)
        const formattedContent = this.formatMessage(content);
        messageContent.innerHTML = formattedContent;

        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = new Date().toLocaleTimeString('id-ID', {
            hour: '2-digit',
            minute: '2-digit'
        });

        if (role === 'user') {
            messageDiv.appendChild(messageContent);
            messageDiv.appendChild(avatar);
        } else {
            messageDiv.appendChild(avatar);
            messageDiv.appendChild(messageContent);
        }

        messageContent.appendChild(messageTime);
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    formatMessage(content) {
        // Basic markdown formatting
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br>');
    }

    setLoading(loading) {
        this.isLoading = loading;
        this.sendBtn.disabled = loading;
        this.loadingIndicator.style.display = loading ? 'flex' : 'none';
        
        if (loading) {
            this.scrollToBottom();
        }
    }

    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }

    async clearChat() {
        if (!confirm('Apakah Anda yakin ingin menghapus semua percakapan?')) {
            return;
        }

        try {
            const response = await fetch('/api/clear', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (response.ok) {
                this.chatMessages.innerHTML = `
                    <div class="welcome-message">
                        <div class="welcome-icon">
                            <i class="fas fa-robot"></i>
                        </div>
                        <h2>Selamat datang di Gemini AI Agent!</h2>
                        <p>Saya siap membantu Anda. Silakan ajukan pertanyaan atau mulai percakapan.</p>
                    </div>
                `;
                this.showToast('Percakapan berhasil dihapus', 'success');
            } else {
                throw new Error('Failed to clear chat');
            }
        } catch (error) {
            console.error('Error clearing chat:', error);
            this.showToast('Gagal menghapus percakapan', 'error');
        }
    }

    async showModelInfo() {
        try {
            const response = await fetch('/api/model-info');
            const data = await response.json();

            let infoHtml = '';
            if (data.error) {
                infoHtml = `<p class="error">Error: ${data.error}</p>`;
            } else {
                infoHtml = `
                    <div class="model-info">
                        <p><strong>Model:</strong> ${data.name || 'Unknown'}</p>
                        <p><strong>Display Name:</strong> ${data.display_name || 'N/A'}</p>
                        <p><strong>Description:</strong> ${data.description || 'N/A'}</p>
                        <p><strong>Input Token Limit:</strong> ${data.input_token_limit || 'Unknown'}</p>
                        <p><strong>Output Token Limit:</strong> ${data.output_token_limit || 'Unknown'}</p>
                    </div>
                `;
            }

            document.getElementById('modelInfo').innerHTML = infoHtml;
            this.modelModal.style.display = 'block';
        } catch (error) {
            console.error('Error fetching model info:', error);
            this.showToast('Gagal mengambil informasi model', 'error');
        }
    }

    closeModal() {
        this.modelModal.style.display = 'none';
    }

    async loadHistory() {
        try {
            const response = await fetch('/api/history');
            const data = await response.json();

            if (data.history && data.history.length > 0) {
                // Remove welcome message
                const welcomeMessage = this.chatMessages.querySelector('.welcome-message');
                if (welcomeMessage) {
                    welcomeMessage.remove();
                }

                // Add messages from history
                data.history.forEach(msg => {
                    if (msg.role === 'user' || msg.role === 'assistant') {
                        this.addMessage(msg.content, msg.role);
                    }
                });
            }
        } catch (error) {
            console.error('Error loading history:', error);
        }
    }

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;

        this.toastContainer.appendChild(toast);

        // Auto remove after 3 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 3000);
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new GeminiChatApp();
});