/*!
 * Amath — widget du chatbot du Ministère de la Fonction Publique.
 *
 * Intégration (une seule ligne, avant </body>) :
 *   <script src="https://<serveur-chatbot>/widget/amath.js" defer
 *           data-endpoint="https://<serveur-chatbot>/api/messages"
 *           data-site="ecarriere"></script>
 *
 * Attributs :
 *   data-endpoint  (obligatoire) URL qui reçoit les messages. Deux formats acceptés :
 *                  - webhook REST de Rasa (réponse : tableau de messages) ;
 *                  - relais Laravel /api/v1/chatbot/messages (réponse : { success, data }).
 *   data-site      identifiant du site (statistiques, préfixe des conversations). Défaut : "web".
 *   data-platform  démarre directement sur une plateforme : "PGDE", "E-Carrière" ou "Attestation".
 *   data-z-index   niveau d'empilement (défaut 1040), à baisser sous les modales du site.
 *   data-position  "right" (défaut) ou "left".
 *   data-label     texte du bouton (défaut : "Besoin d'aide ?").
 *
 * API JavaScript : window.AmathChat.open() / close() / restart().
 *
 * Le widget vit dans un Shadow DOM : le CSS du site ne peut pas le casser, et inversement.
 */
(function () {
    'use strict';

    if (window.AmathChat) { return; } // déjà chargé sur la page

    var script = document.currentScript;
    if (!script || !script.getAttribute('data-endpoint')) {
        if (window.console) { console.error('[Amath] attribut data-endpoint manquant sur la balise <script>.'); }
        return;
    }

    var PLATFORMS = { 'PGDE': 'PGDE', 'E-CARRIERE': 'E-Carrière', 'E-CARRIÈRE': 'E-Carrière', 'ATTESTATION': 'Attestation' };
    var platformAttribute = (script.getAttribute('data-platform') || '').trim().toUpperCase();

    var config = {
        endpoint: script.getAttribute('data-endpoint'),
        site: (script.getAttribute('data-site') || 'web').replace(/[^a-z0-9_-]/gi, '').toLowerCase() || 'web',
        platform: PLATFORMS[platformAttribute] || null,
        zIndex: parseInt(script.getAttribute('data-z-index'), 10) || 1040,
        position: script.getAttribute('data-position') === 'left' ? 'left' : 'right',
        label: script.getAttribute('data-label') || "Besoin d'aide ?"
    };

    var STORAGE_PREFIX = 'amath.' + config.site + '.';
    var SESSION_KEY = STORAGE_PREFIX + 'session_id';
    var HISTORY_KEY = STORAGE_PREFIX + 'history';
    var OPEN_KEY = STORAGE_PREFIX + 'open';
    var MAX_HISTORY = 80;
    var REQUEST_TIMEOUT_MS = 40000;

    // ------------------------------------------------------------------ stockage

    // Le stockage peut être bloqué (navigation privée stricte) : le chat reste utilisable.
    function readStorage(storage, key) {
        try { return storage.getItem(key); } catch (error) { return null; }
    }
    function writeStorage(storage, key, value) {
        try {
            if (value === null) { storage.removeItem(key); } else { storage.setItem(key, value); }
        } catch (error) { /* stockage indisponible */ }
    }

    // Conversation liée à l'onglet (sessionStorage) : sur un poste partagé, la personne
    // suivante ne reprend pas la conversation (CNI vérifiée) de la précédente.
    try { localStorage.removeItem(SESSION_KEY); } catch (error) { /* stockage bloqué */ }

    function newSessionId() {
        if (window.crypto && window.crypto.randomUUID) { return window.crypto.randomUUID(); }
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (character) {
            var random = Math.random() * 16 | 0;
            return (character === 'x' ? random : (random & 0x3 | 0x8)).toString(16);
        });
    }

    function sessionId() {
        var stored = readStorage(sessionStorage, SESSION_KEY);
        if (stored && /^[0-9a-f-]{36}$/i.test(stored)) { return stored; }
        var created = newSessionId();
        writeStorage(sessionStorage, SESSION_KEY, created);
        return created;
    }

    function loadHistory() {
        try { return JSON.parse(readStorage(sessionStorage, HISTORY_KEY)) || []; } catch (error) { return []; }
    }

    // ------------------------------------------------------------------ interface (Shadow DOM)

    var host = document.createElement('amath-chat');
    host.style.cssText = 'position:fixed;bottom:20px;' + config.position + ':20px;z-index:' + config.zIndex + ';';
    var shadow = host.attachShadow({ mode: 'open' });

    var ICONS = {
        chat: '<path d="M4 4h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H9l-5 4v-4H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z"/>',
        restart: '<path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.08A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/>',
        close: '<path d="M19 6.41 17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>',
        send: '<path d="M2.01 21 23 12 2.01 3 2 10l15 2-15 2z"/>'
    };
    // Icônes des boutons, dans le style du site emploi : choisies d'après l'intention
    // du bouton (son payload), jamais d'après son texte.
    var BUTTON_ICON_PATHS = {
        home: 'M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z',
        back: 'M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z',
        support: 'M6.62 10.79a15.05 15.05 0 0 0 6.59 6.59l2.2-2.2a1 1 0 0 1 1.02-.24c1.12.37 2.32.57 3.57.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1.02l-2.2 2.2z',
        retry: 'M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.08A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z',
        check: 'M9 16.17 4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z',
        cross: 'M19 6.41 17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z',
        briefcase: 'M10 4h4a2 2 0 0 1 2 2v1h4a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h4V6a2 2 0 0 1 2-2zm4 3V6h-4v1h4z',
        person: 'M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z',
        document: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z',
        userPlus: 'M15 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8zm-9-2V7H4v3H1v2h3v3h2v-3h3v-2H6zm9 4c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z',
        login: 'M11 7 9.6 8.4l2.6 2.6H2v2h10.2l-2.6 2.6L11 17l5-5-5-5zm9 12h-8v2h8a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2h-8v2h8v14z',
        key: 'M12.65 10A6 6 0 1 0 7 18a6 6 0 0 0 5.65-4H17v4h4v-4h2v-4H12.65zM7 14a2 2 0 1 1 0-4 2 2 0 0 1 0 4z',
        chart: 'M5 9.2h3V19H5zM10.6 5h2.8v14h-2.8zm5.6 8H19v6h-2.8z',
        info: 'M11 7h2v2h-2zm0 4h2v6h-2zm1-9a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 18a8 8 0 1 1 0-16 8 8 0 0 1 0 16z',
        clock: 'M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 18a8 8 0 1 1 0-16 8 8 0 0 1 0 16zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z'
    };
    var BUTTON_ICON_BY_INTENT = {
        go_back_greet_with_name: 'home',
        go_back_ecarriere: 'back',
        go_back_pgde: 'back',
        retour_menu_utilisateur: 'back',
        ask_support: 'support',
        start_account_verification: 'retry',
        confirm_has_account: 'check',
        confirm_has_access: 'check',
        confirm_password_reset: 'check',
        confirm_reset_ecarriere: 'check',
        deny_has_account: 'cross',
        deny_has_access: 'cross',
        deny_password_reset: 'cross',
        cancel_reset_ecarriere: 'cross',
        ask_account_creation: 'userPlus',
        ask_attestation_account: 'userPlus',
        ask_login: 'login',
        ask_password_reset: 'key',
        reset_password_ecarriere: 'key',
        voir_actes: 'document',
        ask_attestation_request: 'document',
        voir_projets: 'chart',
        ask_attestation_info: 'info',
        aucun_projet_acte: 'info',
        ask_attestation_status: 'clock'
    };
    var BUTTON_ICON_BY_PLATFORM = { 'E-Carrière': 'briefcase', 'PGDE': 'person', 'Attestation': 'document' };

    function buttonIconName(payload) {
        var match = /^\/([a-z_]+)(\{.*\})?$/.exec(String(payload || ''));
        if (!match) { return null; }
        if (match[1] === 'choose_platform') {
            try { return BUTTON_ICON_BY_PLATFORM[JSON.parse(match[2]).platform] || null; } catch (error) { return null; }
        }
        return BUTTON_ICON_BY_INTENT[match[1]] || null;
    }

    // Contenu d'un bouton : icône (si connue) + libellé inséré en texte brut.
    function fillChoiceButton(element, button) {
        var iconName = buttonIconName(button.payload);
        if (iconName) {
            element.innerHTML = '<svg class="choice-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
                + '<path d="' + BUTTON_ICON_PATHS[iconName] + '"/></svg>';
        }
        var label = document.createElement('span');
        label.textContent = button.title;
        element.appendChild(label);
    }

    function icon(name) {
        return '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' + ICONS[name] + '</svg>';
    }

    shadow.innerHTML =
        '<style>' + STYLES() + '</style>' +
        '<button type="button" class="toggle" aria-controls="panel" aria-expanded="false" ' +
            'aria-label="Discuter avec Amath, l\'assistant du Ministère">' + icon('chat') +
            '<span class="toggle-label"></span></button>' +
        '<section id="panel" class="panel" role="dialog" aria-label="Amath, assistant du Ministère" hidden>' +
            '<header class="header">' +
                '<div class="title"><span class="avatar" aria-hidden="true">A</span>' +
                    '<div><strong>Amath</strong><small>Assistant du Ministère</small></div></div>' +
                '<div class="actions">' +
                    '<button type="button" class="icon-button" data-action="restart" aria-label="Recommencer la conversation">' + icon('restart') + '</button>' +
                    '<button type="button" class="icon-button" data-action="close" aria-label="Fermer la conversation">' + icon('close') + '</button>' +
                '</div>' +
            '</header>' +
            '<div class="messages" role="log" aria-live="polite" aria-relevant="additions"></div>' +
            '<form class="form" autocomplete="off">' +
                '<label for="input" class="sr-only">Votre message</label>' +
                '<input id="input" class="input" type="text" maxlength="1000" placeholder="Écrivez votre message…" required>' +
                '<button type="submit" class="send" aria-label="Envoyer">' + icon('send') + '</button>' +
            '</form>' +
        '</section>';

    var toggle = shadow.querySelector('.toggle');
    var panel = shadow.querySelector('.panel');
    var messagesBox = shadow.querySelector('.messages');
    var form = shadow.querySelector('.form');
    var input = shadow.querySelector('.input');
    var sendButton = shadow.querySelector('.send');
    shadow.querySelector('.toggle-label').textContent = config.label;

    var history = loadHistory();
    var isSending = false;

    // ------------------------------------------------------------------ rendu

    function saveHistory() {
        history = history.slice(-MAX_HISTORY);
        writeStorage(sessionStorage, HISTORY_KEY, JSON.stringify(history));
    }

    function escapeHtml(text) {
        return String(text)
            .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    }

    // Markdown du bot : le texte est échappé AVANT toute mise en forme (aucune injection HTML possible).
    function renderMarkdown(text) {
        return escapeHtml(text)
            .replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
            .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
            .replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<em>$2</em>')
            .replace(/\n/g, '<br>');
    }

    function scrollToBottom() {
        messagesBox.scrollTop = messagesBox.scrollHeight;
    }

    function renderEntry(entry, isLast) {
        if (entry.text) {
            var bubble = document.createElement('div');
            bubble.className = 'bubble bubble--' + entry.from;
            if (entry.from === 'bot') { bubble.innerHTML = renderMarkdown(entry.text); } else { bubble.textContent = entry.text; }
            messagesBox.appendChild(bubble);
        }
        if (entry.image && /^https?:\/\//.test(entry.image)) {
            var imageBubble = document.createElement('div');
            imageBubble.className = 'bubble bubble--bot';
            var image = document.createElement('img');
            image.src = entry.image;
            image.alt = '';
            imageBubble.appendChild(image);
            messagesBox.appendChild(imageBubble);
        }
        if (entry.buttons && entry.buttons.length) {
            var group = document.createElement('div');
            group.className = 'choices';
            entry.buttons.forEach(function (button) {
                var choice = document.createElement('button');
                choice.type = 'button';
                choice.className = 'choice';
                fillChoiceButton(choice, button);
                choice.disabled = !isLast; // seuls les choix du dernier message restent actifs
                choice.addEventListener('click', function () { sendMessage(button.payload, button.title); });
                group.appendChild(choice);
            });
            messagesBox.appendChild(group);
        }
    }

    // Un menu de boutons attend un choix : la saisie libre est bloquée jusqu'au clic
    // (même comportement que l'ancienne page :8000). Le bouton « recommencer » reste disponible.
    var PLACEHOLDER_TEXT = 'Écrivez votre message…';
    var PLACEHOLDER_CHOICE = 'Utilisez les boutons ci-dessus…';

    function awaitingChoice() {
        var last = history[history.length - 1];
        return Boolean(last && last.from === 'bot' && last.buttons && last.buttons.length);
    }

    function updateComposer() {
        var choiceExpected = !isSending && awaitingChoice();
        input.disabled = isSending || choiceExpected;
        sendButton.disabled = isSending || choiceExpected;
        input.placeholder = choiceExpected ? PLACEHOLDER_CHOICE : PLACEHOLDER_TEXT;
    }

    function renderAll() {
        messagesBox.innerHTML = '';
        history.forEach(function (entry, index) { renderEntry(entry, index === history.length - 1); });
        updateComposer();
        scrollToBottom();
    }

    function addEntry(entry) {
        history.push(entry);
        saveHistory();
        renderAll();
    }

    function setBusy(busy) {
        isSending = busy;
        updateComposer();
        var typing = messagesBox.querySelector('.typing');
        if (busy && !typing) {
            typing = document.createElement('div');
            typing.className = 'typing';
            typing.setAttribute('aria-label', 'Amath écrit');
            typing.innerHTML = '<span></span><span></span><span></span>';
            messagesBox.appendChild(typing);
            scrollToBottom();
        } else if (!busy && typing) {
            typing.parentNode.removeChild(typing);
        }
    }

    // ------------------------------------------------------------------ échanges avec le serveur

    // Accepte la réponse brute de Rasa (tableau) et celle du relais Laravel ({ success, data }).
    function extractMessages(body) {
        if (Array.isArray(body)) {
            return body.map(function (message) {
                return { text: message.text || null, buttons: message.buttons || [], image: message.image || null };
            });
        }
        if (body && body.success && body.data && Array.isArray(body.data.messages)) {
            if (body.data.session_id) { writeStorage(sessionStorage, SESSION_KEY, body.data.session_id); }
            return body.data.messages;
        }
        return null;
    }

    function errorMessage(status, body) {
        if (status === 429) { return 'Vous envoyez beaucoup de messages. Patientez une minute puis réessayez.'; }
        if (status === 503 && body && body.message) { return body.message; }
        return 'Amath est momentanément indisponible. Veuillez réessayer dans quelques instants.';
    }

    function postMessage(message) {
        var currentSession = sessionId();
        // Un seul corps compris par les deux serveurs : Rasa lit sender/message,
        // le relais Laravel lit message/session_id (les champs en trop sont ignorés).
        var body = JSON.stringify({ sender: config.site + '-' + currentSession, message: message, session_id: currentSession });
        var controller = window.AbortController ? new AbortController() : null;
        var timer = controller ? setTimeout(function () { controller.abort(); }, REQUEST_TIMEOUT_MS) : null;

        return fetch(config.endpoint, {
            method: 'POST',
            headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
            body: body,
            signal: controller ? controller.signal : undefined
        }).then(function (response) {
            if (timer) { clearTimeout(timer); }
            return response.json()
                .catch(function () { return null; })
                .then(function (json) { return { status: response.status, body: json }; });
        }, function (error) {
            if (timer) { clearTimeout(timer); }
            throw error;
        });
    }

    function sendMessage(message, displayText) {
        if (isSending || !message) { return; }

        var userWasInChat = shadow.activeElement !== null; // avant setBusy, qui retire le focus du champ
        if (displayText !== null) { addEntry({ from: 'user', text: displayText || message }); }
        setBusy(true);

        postMessage(message)
            .then(function (result) {
                setBusy(false);
                var botMessages = result.status === 200 ? extractMessages(result.body) : null;
                if (!botMessages) {
                    if (result.status === 422) { writeStorage(sessionStorage, SESSION_KEY, null); }
                    addEntry({ from: 'error', text: errorMessage(result.status, result.body) });
                    return;
                }
                botMessages.forEach(function (botMessage) {
                    history.push({ from: 'bot', text: botMessage.text, buttons: botMessage.buttons, image: botMessage.image });
                });
                saveHistory();
                renderAll();
            })
            .catch(function () {
                setBusy(false);
                addEntry({ from: 'error', text: errorMessage(0, null) });
            })
            .then(function () {
                if (!panel.hidden && userWasInChat) { input.focus(); }
            });
    }

    function firstMessage() {
        // Sur un site dédié (ex. E-Carrière), on entre directement dans le bon parcours.
        if (config.platform) { return '/choose_platform{"platform": "' + config.platform + '"}'; }
        return '/greet';
    }

    // ------------------------------------------------------------------ ouverture / fermeture

    // restoring = réouverture automatique au chargement : ne pas voler le focus des formulaires du site.
    function openPanel(restoring) {
        panel.hidden = false;
        toggle.setAttribute('aria-expanded', 'true');
        writeStorage(sessionStorage, OPEN_KEY, '1');
        renderAll();
        if (restoring !== true) { input.focus(); }
        if (history.length === 0) { sendMessage(firstMessage(), null); }
    }

    function closePanel() {
        panel.hidden = true;
        toggle.setAttribute('aria-expanded', 'false');
        writeStorage(sessionStorage, OPEN_KEY, null);
        toggle.focus();
    }

    function restartConversation() {
        writeStorage(sessionStorage, SESSION_KEY, null);
        history = [];
        saveHistory();
        renderAll();
        if (panel.hidden) { openPanel(false); } else { sendMessage(firstMessage(), null); }
    }

    toggle.addEventListener('click', function () { openPanel(false); });
    shadow.querySelector('[data-action="close"]').addEventListener('click', closePanel);
    shadow.querySelector('[data-action="restart"]').addEventListener('click', restartConversation);

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        var text = input.value.trim();
        if (!text) { return; }
        input.value = '';
        sendMessage(text, text);
    });

    panel.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') { closePanel(); }
    });

    function mount() {
        document.body.appendChild(host);
        if (readStorage(sessionStorage, OPEN_KEY) === '1') { openPanel(true); }
    }

    if (document.body) { mount(); } else { document.addEventListener('DOMContentLoaded', mount); }

    window.AmathChat = {
        open: function () { openPanel(false); },
        close: closePanel,
        restart: restartConversation
    };

    // ------------------------------------------------------------------ styles (isolés dans le Shadow DOM)

    function STYLES() {
        return [
            ':host { all: initial; }',
            '*, *::before, *::after { box-sizing: border-box; }',
            ':host, .panel, .toggle, .input, .choice {',
            "  font: 14px/1.5 'DM Sans', system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif;",
            '  color: #282B2D;',
            '}',
            'svg { width: 20px; height: 20px; fill: currentColor; }',
            '.toggle { display: flex; align-items: center; gap: 8px; padding: 12px 18px 12px 14px; border: 3px solid #FCC207;',
            '  border-radius: 999px; background: #00843F; color: #FFFFFF; font-weight: 700; cursor: pointer;',
            '  box-shadow: 0 6px 18px rgba(40, 43, 45, 0.25); transition: background 0.2s, transform 0.2s; }',
            '.toggle:hover { background: #006B33; transform: translateY(-2px); }',
            '.toggle[aria-expanded="true"] { display: none; }',
            '.panel { display: flex; flex-direction: column; width: min(380px, calc(100vw - 40px));',
            '  height: min(600px, calc(100vh - 40px)); background: #FFFFFF; border-radius: 14px; overflow: hidden;',
            '  box-shadow: 0 12px 40px rgba(40, 43, 45, 0.25); }',
            '.panel[hidden] { display: none; }',
            '.header { display: flex; align-items: center; justify-content: space-between; padding: 12px 14px;',
            '  background: #00843F; border-bottom: 3px solid #FCC207; color: #FFFFFF; }',
            '.title { display: flex; align-items: center; gap: 10px; }',
            '.title small { display: block; font-size: 12px; opacity: 0.9; }',
            '.avatar { display: grid; place-items: center; width: 36px; height: 36px; border-radius: 50%;',
            '  background: #FCC207; color: #282B2D; font-weight: 700; }',
            '.actions { display: flex; gap: 4px; }',
            '.icon-button { display: grid; place-items: center; width: 34px; height: 34px; border: 0; border-radius: 8px;',
            '  background: transparent; color: #FFFFFF; cursor: pointer; }',
            '.icon-button:hover { color: #FCC207; background: rgba(255, 255, 255, 0.12); }',
            '.messages { flex: 1; display: flex; flex-direction: column; gap: 10px; padding: 14px; overflow-y: auto; background: #FAFAFA; }',
            '.bubble { max-width: 85%; padding: 10px 12px; border-radius: 12px; word-break: break-word; }',
            '.bubble--bot { align-self: flex-start; background: #FFFFFF; border: 1px solid #E5E5E5; border-bottom-left-radius: 4px; }',
            '.bubble--user { align-self: flex-end; background: #00843F; color: #FFFFFF; border-bottom-right-radius: 4px; }',
            '.bubble--error { align-self: center; max-width: 95%; background: #FDECEE; border-left: 4px solid #ED2939; text-align: center; }',
            '.bubble a { color: #00843F; font-weight: 700; }',
            '.bubble img { display: block; max-width: 100%; border-radius: 8px; }',
            '.choices { display: flex; flex-wrap: wrap; gap: 8px; align-self: flex-start; max-width: 95%; }',
            '.choice { padding: 8px 12px; border: 1px solid #00843F; border-radius: 999px; background: #FFFFFF; color: #00843F;',
            '  font-weight: 600; cursor: pointer; transition: background 0.2s, color 0.2s; }',
            '.choice:hover:not(:disabled) { background: #00843F; color: #FFFFFF; }',
            '.choice:disabled { border-color: #E5E5E5; color: #6C757D; cursor: default; }',
            '.choice { display: inline-flex; align-items: center; gap: 6px; }',
            '.choice-icon { width: 16px; height: 16px; fill: currentColor; flex-shrink: 0; }',
            '.typing { align-self: flex-start; display: flex; gap: 4px; padding: 12px; }',
            '.typing span { width: 8px; height: 8px; border-radius: 50%; background: #00843F; animation: bounce 1.2s infinite ease-in-out both; }',
            '.typing span:nth-child(2) { animation-delay: 0.15s; }',
            '.typing span:nth-child(3) { animation-delay: 0.3s; }',
            '@keyframes bounce { 0%, 80%, 100% { transform: scale(0.4); } 40% { transform: scale(1); } }',
            '.form { display: flex; gap: 8px; padding: 12px; border-top: 1px solid #E5E5E5; background: #FFFFFF; }',
            '.input { flex: 1; min-width: 0; padding: 10px 12px; border: 1px solid #E5E5E5; border-radius: 10px; background: #FFFFFF; }',
            '.input::placeholder { color: #6C757D; }',
            '.input:focus { outline: none; border-color: #00843F; box-shadow: 0 0 0 3px rgba(0, 132, 63, 0.18); }',
            '.send { display: grid; place-items: center; width: 44px; border: 0; border-radius: 10px; background: #00843F; color: #FFFFFF; cursor: pointer; }',
            '.send:hover:not(:disabled) { background: #006B33; }',
            '.send:disabled, .input:disabled { opacity: 0.55; cursor: not-allowed; }',
            'button:focus-visible, .input:focus-visible { outline: 3px solid #FCC207; outline-offset: 2px; }',
            '.sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }',
            '@media (max-width: 640px) {',
            '  .toggle-label { display: none; }',
            '  .toggle { padding: 14px; }',
            '  .panel { position: fixed; inset: 0; width: 100%; height: 100%; border-radius: 0; }',
            '}',
            '@media print { :host { display: none !important; } }'
        ].join('\n');
    }
})();
