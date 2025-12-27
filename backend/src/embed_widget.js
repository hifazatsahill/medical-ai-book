// RAG Chatbot Embed Widget
// This script allows the RAG chatbot to be embedded in HTML books

class RAGChatbotWidget {
  constructor(config = {}) {
    this.config = {
      apiUrl: config.apiUrl || 'http://localhost:8000',
      collectionId: config.collectionId,
      containerId: config.containerId || 'rag-chatbot-container',
      theme: config.theme || 'light',
      ...config
    };

    this.sessionId = this.generateSessionId();
    this.isOpen = false;
    this.initializeWidget();
  }

  generateSessionId() {
    // Generate a random UUID for the session
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0;
      const v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }

  initializeWidget() {
    // Create the widget container if it doesn't exist
    let container = document.getElementById(this.config.containerId);
    if (!container) {
      container = document.createElement('div');
      container.id = this.config.containerId;
      document.body.appendChild(container);
    }

    // Add CSS styles
    this.addStyles();

    // Create the widget HTML
    container.innerHTML = `
      <div id="rag-chatbot-widget" class="rag-chatbot-widget ${this.config.theme}-theme">
        <div id="rag-chatbot-toggle" class="rag-chatbot-toggle">
          <span>📚 Ask Book</span>
        </div>
        <div id="rag-chatbot-panel" class="rag-chatbot-panel">
          <div class="rag-chatbot-header">
            <h3>Book Assistant</h3>
            <button id="rag-chatbot-close" class="rag-chatbot-close">✕</button>
          </div>
          <div id="rag-chatbot-messages" class="rag-chatbot-messages">
            <div class="rag-chatbot-message system-message">
              Hello! I'm your book assistant. Ask me anything about this book.
            </div>
          </div>
          <div class="rag-chatbot-input-area">
            <textarea 
              id="rag-chatbot-input" 
              class="rag-chatbot-input" 
              placeholder="Ask a question about the book..."
              rows="2"
            ></textarea>
            <button id="rag-chatbot-send" class="rag-chatbot-send">Send</button>
          </div>
        </div>
      </div>
    `;

    // Add event listeners
    this.addEventListeners();
  }

  addStyles() {
    // Check if styles are already added
    if (document.getElementById('rag-chatbot-styles')) {
      return;
    }

    const styles = document.createElement('style');
    styles.id = 'rag-chatbot-styles';
    styles.textContent = `
      .rag-chatbot-widget {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 10000;
        font-family: Arial, sans-serif;
      }

      .rag-chatbot-toggle {
        position: absolute;
        bottom: 0;
        right: 0;
        background: #4f46e5;
        color: white;
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        font-weight: bold;
        font-size: 14px;
      }

      .rag-chatbot-panel {
        position: absolute;
        bottom: 70px;
        right: 0;
        width: 350px;
        height: 500px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
        display: none;
        flex-direction: column;
        overflow: hidden;
      }

      .rag-chatbot-panel.open {
        display: flex;
      }

      .rag-chatbot-header {
        background: #4f46e5;
        color: white;
        padding: 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }

      .rag-chatbot-close {
        background: none;
        border: none;
        color: white;
        font-size: 18px;
        cursor: pointer;
      }

      .rag-chatbot-messages {
        flex: 1;
        padding: 15px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 10px;
      }

      .rag-chatbot-message {
        max-width: 80%;
        padding: 10px 15px;
        border-radius: 18px;
        font-size: 14px;
        line-height: 1.4;
      }

      .user-message {
        align-self: flex-end;
        background: #4f46e5;
        color: white;
      }

      .assistant-message {
        align-self: flex-start;
        background: #f3f4f6;
        color: #374151;
      }

      .system-message {
        align-self: center;
        background: #dbeafe;
        color: #1e40af;
        font-style: italic;
      }

      .rag-chatbot-input-area {
        padding: 15px;
        border-top: 1px solid #e5e7eb;
        display: flex;
        gap: 10px;
      }

      .rag-chatbot-input {
        flex: 1;
        padding: 10px;
        border: 1px solid #d1d5db;
        border-radius: 5px;
        resize: none;
      }

      .rag-chatbot-send {
        background: #4f46e5;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 15px;
        cursor: pointer;
      }

      .rag-chatbot-send:hover {
        background: #4338ca;
      }

      .rag-chatbot-widget.light-theme {
        /* Light theme styles (default) */
      }

      .rag-chatbot-widget.dark-theme {
        /* Dark theme styles would go here */
      }
    `;

    document.head.appendChild(styles);
  }

  addEventListeners() {
    const toggleButton = document.getElementById('rag-chatbot-toggle');
    const closeButton = document.getElementById('rag-chatbot-close');
    const sendButton = document.getElementById('rag-chatbot-send');
    const input = document.getElementById('rag-chatbot-input');
    const panel = document.getElementById('rag-chatbot-panel');

    toggleButton.addEventListener('click', () => this.toggleWidget());
    closeButton.addEventListener('click', () => this.closeWidget());
    sendButton.addEventListener('click', () => this.sendMessage());
    
    // Allow sending with Enter key (without Shift)
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this.sendMessage();
      }
    });
  }

  toggleWidget() {
    const panel = document.getElementById('rag-chatbot-panel');
    this.isOpen = !this.isOpen;
    
    if (this.isOpen) {
      panel.classList.add('open');
    } else {
      panel.classList.remove('open');
    }
  }

  closeWidget() {
    const panel = document.getElementById('rag-chatbot-panel');
    panel.classList.remove('open');
    this.isOpen = false;
  }

  async sendMessage() {
    const input = document.getElementById('rag-chatbot-input');
    const message = input.value.trim();
    
    if (!message) return;

    // Add user message to UI
    this.addMessage(message, 'user');
    input.value = '';

    try {
      // Get selected text if any
      const selectedText = this.getSelectedText();

      // Send the query to the backend
      const response = await this.queryBackend(message, selectedText);

      // Add assistant response to UI
      this.addMessage(response.response, 'assistant');
    } catch (error) {
      console.error('Error sending message:', error);
      this.addMessage('Sorry, I encountered an error processing your request.', 'assistant');
    }
  }

  getSelectedText() {
    const selection = window.getSelection();
    return selection.toString().trim();
  }

  async queryBackend(query, selectedText = null) {
    const response = await fetch(`${this.config.apiUrl}/v1/collections/${this.config.collectionId}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: query,
        sessionId: this.sessionId,
        selectedText: selectedText || undefined
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  addMessage(text, sender) {
    const messagesContainer = document.getElementById('rag-chatbot-messages');
    
    const messageElement = document.createElement('div');
    messageElement.classList.add('rag-chatbot-message');
    messageElement.classList.add(sender === 'user' ? 'user-message' : 
                                 sender === 'assistant' ? 'assistant-message' : 'system-message');
    messageElement.textContent = text;
    
    messagesContainer.appendChild(messageElement);
    
    // Scroll to the bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }
}

// Initialize the widget when the script is loaded
document.addEventListener('DOMContentLoaded', function() {
  // Look for config in a script tag or window object
  const config = window.RAG_CHATBOT_CONFIG || {};
  new RAGChatbotWidget(config);
});

// Make the class available globally
window.RAGChatbotWidget = RAGChatbotWidget;