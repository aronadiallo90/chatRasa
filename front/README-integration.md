# Amath Chatbot - Guide d'intégration

## Fichiers du chatbot

Le chatbot Amath est composé de 3 fichiers principaux :
- `chatbot-amath.css` - Styles avec préfixes spécifiques
- `chatbot-amath.js` - Logique JavaScript avec namespace AmathChatbot
- `chatbot-amath.html` - Page complète pour test/démo

## Intégration sur un site externe

### Méthode 1 : Widget automatique (Recommandée)

```html
<!-- Ajouter à la fin de votre page, avant </body> -->
<script src="path/to/amath-chatbot-widget.js"></script>
<script>
    AmathChatbotWidget.init({
        serverUrl: "https://votre-serveur-rasa.com/webhooks/rest/webhook",
        botTitle: "Assistant Amath"
    });
</script>
```

### Méthode 2 : Intégration manuelle

```html
<!-- Dans le <head> -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
<link rel="stylesheet" href="path/to/chatbot-amath.css">

<!-- À la fin du <body> -->
<div class="amath-chatbot-container">
    <div class="amath-chatbot-header">
        <span><i class="fas fa-robot"></i> Amath (MFPRSP)</span>
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

<script src="path/to/chatbot-amath.js"></script>
<script>
    AmathChatbot.init({
        serverUrl: "https://votre-serveur-rasa.com/webhooks/rest/webhook",
        trackerUrl: "https://votre-serveur-rasa.com/conversations"
    });
</script>
```

## Configuration

### Options disponibles

```javascript
AmathChatbot.init({
    serverUrl: "http://localhost:5005/webhooks/rest/webhook", // URL de votre serveur Rasa
    trackerUrl: "http://localhost:5005/conversations",        // URL pour reset session
    botTitle: "Amath (MFPRSP)"                               // Titre affiché
});
```

## API JavaScript

### Méthodes disponibles

```javascript
// Ouvrir le chatbot
AmathChatbot.openChat();

// Fermer le chatbot
AmathChatbot.closeChat();

// Redémarrer la conversation
AmathChatbot.restartChat();

// Envoyer un message programmatiquement
AmathChatbot.sendMessage("Bonjour");
```

## Caractéristiques anti-conflit

### CSS
- Toutes les classes CSS sont préfixées par `amath-chatbot-`
- Z-index élevé (10000) pour éviter les superpositions
- Styles encapsulés avec font-family héritée

### JavaScript
- Namespace `AmathChatbot` pour éviter les conflits globaux
- Session storage avec préfixe `amath_`
- Event handlers délégués pour éviter les conflits

### Exemples de classes CSS
```css
.amath-chatbot-container
.amath-chatbot-header
.amath-chatbot-message
.amath-chatbot-button
```

## Déploiement

1. Uploadez les fichiers sur votre serveur :
   - `chatbot-amath.css`
   - `chatbot-amath.js`
   - `amath-chatbot-widget.js` (optionnel)

2. Modifiez l'URL du serveur Rasa dans la configuration

3. Intégrez le code dans vos pages web

## Personnalisation

### Couleurs principales
Les couleurs peuvent être modifiées dans le fichier CSS :
- Vert principal : `#00843F`
- Vert hover : `#006d32`
- Messages utilisateur : `#00843F`

### Responsive
Le chatbot est entièrement responsive avec des breakpoints à :
- Mobile : < 640px
- Tablet : 640px - 1024px
- Desktop : > 1024px

## Dépendances

- Font Awesome 6.0.0+ (chargé automatiquement)
- Navigateurs modernes (ES6+)

## Support

Le chatbot supporte :
- Messages texte
- Boutons interactifs
- Messages d'erreur/info
- Indicateur de chargement
- Session persistante
- Reset de conversation