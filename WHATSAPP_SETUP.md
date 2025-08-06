# 📱 Guide d'intégration WhatsApp pour votre Chatbot Rasa

## 🎯 Vue d'ensemble

Ce guide vous explique comment déployer votre chatbot Rasa existant sur WhatsApp Business API.

## 📋 Prérequis

### 1. Compte Meta Business
- Créer un compte Meta Business sur [business.facebook.com](https://business.facebook.com)
- Ajouter votre numéro de téléphone professionnel
- Vérification d'entreprise requise

### 2. Configuration WhatsApp Business API
1. Aller sur [developers.facebook.com](https://developers.facebook.com)
2. Créer une nouvelle app → "Business" → "WhatsApp"
3. Configurer WhatsApp Business API
4. Obtenir vos credentials :
   - `access_token` (Token d'accès permanent)
   - `phone_number_id` (ID du numéro de téléphone)
   - `verify_token` (Token de vérification webhook)

## 🔧 Installation

### 1. Dépendances Python
```bash
pip install flask requests
```

### 2. Configuration des credentials

Modifiez le fichier `credentials.yml` :
```yaml
whatsapp:
  access_token: "VOTRE_ACCESS_TOKEN"
  phone_number_id: "VOTRE_PHONE_NUMBER_ID"  
  verify_token: "VOTRE_VERIFY_TOKEN"
  webhook_url: "/webhooks/whatsapp/webhook"
```

### 3. Variables d'environnement (recommandé)
```bash
export WHATSAPP_ACCESS_TOKEN="votre_token"
export WHATSAPP_PHONE_NUMBER_ID="votre_phone_id"
export WHATSAPP_VERIFY_TOKEN="votre_verify_token"
```

## 🚀 Déploiement

### Option 1 : Test local avec ngrok

1. **Installer ngrok** : [ngrok.com](https://ngrok.com)

2. **Démarrer le bot** :
```bash
python run_whatsapp.py
```

3. **Exposer le port avec ngrok** :
```bash
ngrok http 5005
```

4. **Configurer le webhook dans Meta** :
   - URL : `https://VOTRE_URL_NGROK.ngrok.io/webhooks/whatsapp/webhook`
   - Token de vérification : Votre `verify_token`

### Option 2 : Déploiement en production

#### Heroku
1. **Créer l'app Heroku** :
```bash
heroku create votre-bot-whatsapp
```

2. **Configurer les variables** :
```bash
heroku config:set WHATSAPP_ACCESS_TOKEN=votre_token
heroku config:set WHATSAPP_PHONE_NUMBER_ID=votre_phone_id
heroku config:set WHATSAPP_VERIFY_TOKEN=votre_verify_token
```

3. **Deployer** :
```bash
git add .
git commit -m "Add WhatsApp integration"
git push heroku main
```

4. **URL webhook** : `https://votre-bot-whatsapp.herokuapp.com/webhooks/whatsapp/webhook`

#### VPS/Serveur dédié
1. **Configuration HTTPS** (obligatoire pour WhatsApp) :
```bash
# Avec nginx + Let's Encrypt
sudo apt install nginx certbot python3-certbot-nginx
sudo certbot --nginx -d votre-domaine.com
```

2. **Service systemd** :
```bash
sudo nano /etc/systemd/system/whatsapp-bot.service
```
```ini
[Unit]
Description=Rasa WhatsApp Bot
After=network.target

[Service]
Type=simple
User=votre-utilisateur
WorkingDirectory=/path/to/your/bot
ExecStart=/usr/bin/python3 run_whatsapp.py
Restart=always

[Install]
WantedBy=multi-user.target
```

3. **Démarrer le service** :
```bash
sudo systemctl enable whatsapp-bot
sudo systemctl start whatsapp-bot
```

## 🔒 Configuration Webhook Meta

### 1. Console Meta for Developers
1. Aller dans votre app WhatsApp
2. Configuration → Webhooks
3. URL : `https://votre-domaine.com/webhooks/whatsapp/webhook`
4. Token de vérification : Votre `verify_token`
5. Champs à souscrire : `messages`

### 2. Test de vérification
Le webhook doit répondre avec le `challenge` pour validation.

## 📱 Test de l'intégration

### 1. Numéro de test
- Utilisez le numéro WhatsApp configuré dans Meta
- Envoyez un message : "Bonjour"
- Le bot doit répondre avec le menu principal

### 2. Debug
```bash
# Logs en temps réel
tail -f /var/log/whatsapp-bot.log

# Test de connectivité
curl -X GET "https://votre-domaine.com/health"
```

## 🔧 Fonctionnalités supportées

### ✅ Supporté
- Messages texte
- Boutons interactifs (max 3)
- Réponses rapides
- Gestion des erreurs

### ⚠️ Limitations WhatsApp
- Max 3 boutons par message
- Titre bouton : 20 caractères max
- Pas de carousels natifs

## 🛠️ Maintenance

### 1. Renouvellement des tokens
- Les tokens d'accès expirent (généralement 60 jours)
- Configurer le renouvellement automatique
- Surveiller les logs d'erreur 401

### 2. Monitoring
```bash
# Statut du service
sudo systemctl status whatsapp-bot

# Métriques
curl https://votre-domaine.com/health
```

## 🐛 Dépannage

### Erreurs courantes

1. **Webhook non vérifié** :
   - Vérifier l'URL HTTPS
   - Contrôler le `verify_token`

2. **Messages non reçus** :
   - Vérifier les permissions webhook
   - Contrôler les logs du serveur

3. **Token expiré** :
   - Régénérer depuis Meta for Developers
   - Mettre à jour les variables d'environnement

### Logs utiles
```python
# Activer debug dans run_whatsapp.py
app.run(host="0.0.0.0", port=port, debug=True)
```

## 📞 Support

Pour obtenir de l'aide :
1. Vérifier les logs : `tail -f logs/whatsapp.log`
2. Tester l'endpoint : `/health` 
3. Consulter Meta for Developers docs

## 🔄 Mise à jour

Pour mettre à jour le connecteur :
```bash
git pull origin main
pip install -r requirements.txt
sudo systemctl restart whatsapp-bot
```

---

🎉 **Félicitations !** Votre chatbot est maintenant disponible sur WhatsApp !