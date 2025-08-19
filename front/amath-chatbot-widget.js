/**
 * Amath Chatbot Widget - Script d'intégration pour sites externes
 * 
 * Usage:
 * <script src="amath-chatbot-widget.js"></script>
 * <script>
 *   AmathChatbotWidget.init({
 *     serverUrl: "https://votre-serveur.com/webhooks/rest/webhook", // optionnel
 *     botTitle: "Mon Assistant" // optionnel
 *   });
 * </script>
 */

(function() {
    'use strict';
    
    window.AmathChatbotWidget = {
        init: function(config = {}) {
            // Configuration par défaut
            const defaultConfig = {
                serverUrl: "http://localhost:5005/webhooks/rest/webhook",
                trackerUrl: "http://localhost:5005/conversations",
                botTitle: "Amath (MFPRSP)",
                cssUrl: "./chatbot-amath.css", // URL relative ou absolue du CSS
                jsUrl: "./chatbot-amath.js"    // URL relative ou absolue du JS
            };
            
            const finalConfig = Object.assign({}, defaultConfig, config);
            
            // Charger le CSS
            this.loadCSS(finalConfig.cssUrl);
            
            // Charger le JavaScript et initialiser
            this.loadJS(finalConfig.jsUrl, function() {
                // Injecter le HTML
                AmathChatbotWidget.injectHTML(finalConfig.botTitle);
                
                // Attendre un peu puis initialiser le chatbot
                setTimeout(function() {
                    if (window.AmathChatbot) {
                        AmathChatbot.init({
                            serverUrl: finalConfig.serverUrl,
                            trackerUrl: finalConfig.trackerUrl,
                            botTitle: finalConfig.botTitle
                        });
                    } else {
                        console.error('AmathChatbot non disponible après chargement');
                    }
                }, 100);
            });
        },
        
        loadCSS: function(url) {
            if (document.querySelector('link[href="' + url + '"]')) return;
            
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.type = 'text/css';
            link.href = url;
            document.head.appendChild(link);
        },
        
        loadJS: function(url, callback) {
            if (document.querySelector('script[src="' + url + '"]')) {
                if (callback) callback();
                return;
            }
            
            const script = document.createElement('script');
            script.type = 'text/javascript';
            script.src = url;
            script.onload = callback;
            document.head.appendChild(script);
        },
        
        injectHTML: function(botTitle) {
            // Vérifier si le chatbot est déjà injecté
            if (document.querySelector('.amath-chatbot-container')) return;
            
            // Charger Font Awesome si pas déjà présent
            if (!document.querySelector('link[href*="font-awesome"]')) {
                this.loadCSS('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
            }
            
            const chatbotHTML = `
                <div class="amath-chatbot-container">
                    <div class="amath-chatbot-header">
                        <span><i class="fas fa-robot"></i> ${botTitle}</span>
                        <div class="amath-chatbot-header-actions">
                            <button onclick="AmathChatbot.restartChat()"><i class="fas fa-sync"></i></button>
                            <button onclick="AmathChatbot.closeChat()"><i class="fas fa-times"></i></button>
                        </div>
                    </div>
                    <div class="amath-chatbot-box"></div>
                    <div class="amath-chatbot-input-container">
                        <input type="text" class="amath-chatbot-user-input" placeholder="Tapez votre message...">
                        <button class="amath-chatbot-send-button"><i class="fas fa-paper-plane"></i></button>
                    </div>
                </div>

                <div class="amath-chatbot-actions">
                    <div class="amath-chatbot-icon" onclick="AmathChatbot.openChat()">
                        <i class="fas fa-comments"></i>
                    </div>
                </div>
            `;
            
            // Injecter le HTML à la fin du body
            document.body.insertAdjacentHTML('beforeend', chatbotHTML);
        }
    };
})();