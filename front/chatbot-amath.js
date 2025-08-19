/**
 * Amath Chatbot - Version intégrable
 * Namespace: AmathChatbot pour éviter les conflits
 */
window.AmathChatbot = (function() {
    'use strict';
    
    // Variables privées
    let lastButtons = [];
    let loadingIndicator;
    let senderId = sessionStorage.getItem('amath_sender_id') || generateUUID();
    sessionStorage.setItem('amath_sender_id', senderId);
    
    // Configuration par défaut (peut être surchargée)
    const config = {
        serverUrl: "http://localhost:5005/webhooks/rest/webhook",
        trackerUrl: "http://localhost:5005/conversations",
        botTitle: "Amath (MFPRSP)"
    };
    
    function generateUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            const r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }
    
    function appendMessage(text, sender) {
        let chatBox = document.querySelector(".amath-chatbot-box");
        if (!chatBox) return;
        
        let messageDiv = document.createElement("div");
        let messageClass = "amath-chatbot-message ";
        
        switch(sender) {
            case "bot":
                messageClass += "amath-chatbot-bot-message";
                break;
            case "error":
                messageClass += "amath-chatbot-error-message";
                break;
            case "info":
                messageClass += "amath-chatbot-info-message";
                break;
            default:
                messageClass += "amath-chatbot-user-message";
        }
        
        messageDiv.className = messageClass;
        
        let formattedText = text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\[([^\]]+)\]\((https?:\/\/[^\s]+)\)/g, '<a href="$2" target="_blank" style="text-decoration: underline; color: #3b82f6;">$1</a>')
            .replace(/\n/g, '<br>');
        
        messageDiv.innerHTML = formattedText;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    
    function appendButtons(buttons) {
        let chatBox = document.querySelector(".amath-chatbot-box");
        if (!chatBox) return;
        
        let buttonContainer = document.createElement("div");
        buttonContainer.className = "amath-chatbot-button-container";

        buttons.forEach(button => {
            let buttonElement = document.createElement("button");
            buttonElement.className = "amath-chatbot-button";
            buttonElement.innerText = button.title;
            buttonElement.onclick = () => {
                appendMessage(button.title, "user");
                disableButtons();
                sendMessage(button.payload);
            };
            buttonContainer.appendChild(buttonElement);
        });

        lastButtons = buttonContainer;
        chatBox.appendChild(buttonContainer);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    
    function disableButtons() {
        if (lastButtons && lastButtons.children) {
            Array.from(lastButtons.children).forEach(btn => btn.disabled = true);
        }
    }
    
    function enableInput() {
        let userInput = document.querySelector(".amath-chatbot-user-input");
        let sendButton = document.querySelector(".amath-chatbot-send-button");
        
        if (userInput) {
            userInput.disabled = false;
            userInput.placeholder = "Tapez votre message...";
        }
        if (sendButton) {
            sendButton.disabled = false;
        }
    }
    
    function disableInput() {
        let userInput = document.querySelector(".amath-chatbot-user-input");
        let sendButton = document.querySelector(".amath-chatbot-send-button");
        
        if (userInput) {
            userInput.disabled = true;
            userInput.placeholder = "Utilisez les boutons ci-dessus...";
        }
        if (sendButton) {
            sendButton.disabled = true;
        }
    }
    
    function showLoadingIndicator() {
        let chatBox = document.querySelector(".amath-chatbot-box");
        if (!chatBox) return;
        
        loadingIndicator = document.createElement("div");
        loadingIndicator.className = "amath-chatbot-loading-indicator";
        loadingIndicator.innerHTML = '<span class="amath-chatbot-dot"></span><span class="amath-chatbot-dot"></span><span class="amath-chatbot-dot"></span>';
        chatBox.appendChild(loadingIndicator);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    
    function hideLoadingIndicator() {
        if (loadingIndicator) {
            loadingIndicator.remove();
            loadingIndicator = null;
        }
    }
    
    function sendMessage(payload) {
        showLoadingIndicator();
        fetch(config.serverUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ sender: senderId, message: payload })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erreur HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            hideLoadingIndicator();
            if (data.length === 0) {
                appendMessage("réessayer", "info");
                return;
            }
            let foundButtons = false;
            data.forEach(res => {
                if (res.text) appendMessage(res.text, "bot");
                if (res.buttons) {
                    foundButtons = true;
                    appendButtons(res.buttons);
                }
            });
            
            if (foundButtons) {
                disableInput();
            } else {
                enableInput();
            }
        })
        .catch(error => {
            hideLoadingIndicator();
            console.error("Erreur Amath Chatbot:", error);
            appendMessage("Impossible de contacter le serveur. Veuillez vérifier votre connexion ou réessayer plus tard.", "error");
        });
    }
    
    function sendUserMessage() {
        let userInput = document.querySelector(".amath-chatbot-user-input");
        let sendButton = document.querySelector(".amath-chatbot-send-button");
        
        if (!userInput || !sendButton) return;
        if (userInput.disabled || sendButton.disabled) return;
        
        let message = userInput.value.trim();
        if (message === "") return;
        
        disableButtons();
        appendMessage(message, "user");
        sendMessage(message);
        userInput.value = "";
    }
    
    function restartChat() {
        let chatBox = document.querySelector(".amath-chatbot-box");
        if (chatBox) {
            chatBox.innerHTML = "";
        }
        
        enableInput();
        
        fetch(`${config.trackerUrl}/${senderId}/tracker/events`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                "event": "restart",
                "timestamp": Date.now() / 1000
            })
        })
        .then(() => {
            senderId = generateUUID();
            sessionStorage.setItem('amath_sender_id', senderId);
            sendMessage("/greet");
        })
        .catch(error => {
            console.warn("Erreur lors de la réinitialisation de la session:", error);
            senderId = generateUUID();
            sessionStorage.setItem('amath_sender_id', senderId);
            sendMessage("/greet");
        });
    }
    
    function closeChat() {
        let chatContainer = document.querySelector(".amath-chatbot-container");
        let chatIcon = document.querySelector(".amath-chatbot-icon");
        
        if (chatContainer) chatContainer.style.display = "none";
        if (chatIcon) chatIcon.style.display = "flex";
    }
    
    function openChat() {
        let chatContainer = document.querySelector(".amath-chatbot-container");
        let chatIcon = document.querySelector(".amath-chatbot-icon");
        
        if (chatContainer) chatContainer.style.display = "flex";
        if (chatIcon) chatIcon.style.display = "none";
    }
    
    function initializeEventHandlers() {
        // Event handler pour l'input (Enter key)
        document.addEventListener('keydown', function(event) {
            if (event.target.classList.contains('amath-chatbot-user-input') && event.key === 'Enter') {
                sendUserMessage();
            }
        });
        
        // Event handlers pour les boutons (utilisation de délégation d'événements)
        document.addEventListener('click', function(event) {
            if (event.target.classList.contains('amath-chatbot-send-button')) {
                sendUserMessage();
            }
        });
    }
    
    function initialize(customConfig = {}) {
        // Fusionner la configuration personnalisée
        Object.assign(config, customConfig);
        
        // Initialiser les event handlers
        initializeEventHandlers();
        
        // Démarrer la conversation
        sendMessage("/greet");
    }
    
    // API publique
    return {
        init: initialize,
        openChat: openChat,
        closeChat: closeChat,
        restartChat: restartChat,
        sendMessage: sendMessage,
        config: config
    };
})();