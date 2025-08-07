# 🚀 Guide Complet : Déployer votre Chatbot Rasa sur WhatsApp avec Ultramsg

## 📋 **ÉTAPES À SUIVRE**

### ✅ **1. Vérifier les prérequis**
```bash
# Dans le répertoire de votre projet
cd C:\Users\Arona\Desktop\fp\test\pycharm\pycharm

# Installer les nouvelles dépendances
pip install python-dotenv requests flask

# Vérifier que Rasa fonctionne
rasa train
```

### ✅ **2. Configurer vos credentials Ultramsg**

**Étape 2.1 :** Modifier le fichier `.env` avec vos vraies informations
```bash
# Ouvrir le fichier .env et remplacer par vos vraies valeurs
ULTRAMSG_TOKEN=VOTRE_VRAI_TOKEN
ULTRAMSG_INSTANCE_ID=VOTRE_VRAIE_INSTANCE
```

**Étape 2.2 :** Tester la configuration
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Token:', os.getenv('ULTRAMSG_TOKEN'))"
```

### ✅ **3. Démarrer le bot en local**

```bash
# Démarrer le nouveau script
python run_ultramsg.py
```

**Vous devriez voir :**
```
🚀 Démarrage du chatbot Rasa avec Ultramsg WhatsApp...
📦 Chargement du modèle: models/20250807-093031-wary-swamp.tar.gz
✅ Modèle chargé avec succès
✅ Credentials Ultramsg configurés
🌐 Serveur démarré sur le port 5005
📱 Webhook Ultramsg: http://localhost:5005/webhooks/ultramsg/webhook
✅ Bot prêt à recevoir des messages WhatsApp!
```

### ✅ **4. Exposer votre serveur local**

**Option A : Avec ngrok (recommandé pour tests)**
```bash
# Installer ngrok : https://ngrok.com/download
ngrok http 5005
```

**Copier l'URL HTTPS fournie :** `https://abc123.ngrok.io`

**Option B : Déploiement sur serveur**
- VPS/Serveur dédié avec domaine et HTTPS
- Heroku, DigitalOcean, etc.

### ✅ **5. Configurer le webhook dans Ultramsg**

1. **Aller sur votre dashboard Ultramsg**
2. **Configurer le webhook :**
   - URL : `https://VOTRE_URL.ngrok.io/webhooks/ultramsg/webhook`
   - Méthode : POST
   - Événements : Message reçu

3. **Tester le webhook :**
```bash
curl -X POST https://VOTRE_URL.ngrok.io/webhooks/ultramsg/webhook \
  -H "Content-Type: application/json" \
  -d '{"from": "212600000000", "body": "test", "type": "text"}'
```

### ✅ **6. Test complet**

1. **Envoyer un message WhatsApp** au numéro connecté à votre instance Ultramsg
2. **Message suggéré :** "Bonjour"
3. **Le bot devrait répondre** avec le menu principal de votre chatbot

### ✅ **7. Monitoring et logs**

**Vérifier que tout fonctionne :**
```bash
# État du serveur
curl http://localhost:5005/health

# Logs en temps réel
# Regarder la console où vous avez lancé run_ultramsg.py
```

## 🐛 **Dépannage**

### ❌ **Problème : "Aucun modèle trouvé"**
```bash
# Entraîner un nouveau modèle
rasa train
```

### ❌ **Problème : "Credentials manquants"**
1. Vérifier le fichier `.env`
2. Vérifier que le token Ultramsg est correct
3. Vérifier que l'instance ID est correct

### ❌ **Problème : "Le bot ne répond pas"**
1. Vérifier que le webhook est configuré dans Ultramsg
2. Vérifier les logs du serveur
3. Tester l'URL du webhook manuellement

### ❌ **Problème : "Erreur de connexion"**
1. Vérifier que ngrok fonctionne
2. Vérifier que l'URL HTTPS est accessible
3. Vérifier les paramètres firewall

## 🔧 **Configuration avancée**

### **Variables d'environnement complètes (.env) :**
```env
# Ultramsg Configuration
ULTRAMSG_TOKEN=votre_token_ultramsg
ULTRAMSG_INSTANCE_ID=votre_instance_id
ULTRAMSG_BASE_URL=https://api.ultramsg.com

# Serveur Configuration
PORT=5005
WEBHOOK_VERIFY_TOKEN=mon_token_secret_123

# Mode (True pour dev, False pour production)
DEBUG_MODE=True

# Optionnel : Base de données
DATABASE_URL=sqlite:///chatbot.db
```

### **Déploiement en production :**

**Sur serveur Linux :**
```bash
# Créer un service systemd
sudo nano /etc/systemd/system/rasa-ultramsg.service

[Unit]
Description=Rasa Ultramsg WhatsApp Bot
After=network.target

[Service]
Type=simple
User=votre-utilisateur
WorkingDirectory=/chemin/vers/votre/projet
ExecStart=/usr/bin/python3 run_ultramsg.py
Restart=always
Environment=DEBUG_MODE=False

[Install]
WantedBy=multi-user.target
```

```bash
# Activer et démarrer
sudo systemctl enable rasa-ultramsg
sudo systemctl start rasa-ultramsg
sudo systemctl status rasa-ultramsg
```

## 🎉 **Félicitations !**

Votre chatbot Rasa est maintenant disponible sur WhatsApp via Ultramsg !

**Fonctionnalités disponibles :**
- ✅ Messages texte
- ✅ Réponses automatiques
- ✅ Gestion des intents et entities
- ✅ Boutons simulés (liste numérotée)
- ✅ Actions personnalisées
- ✅ Monitoring et logs

**Pour aller plus loin :**
- Ajouter des images et fichiers
- Intégrer une base de données
- Ajouter des métriques d'utilisation
- Déployer en haute disponibilité