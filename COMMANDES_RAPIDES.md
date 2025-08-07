# ⚡ Commandes Rapides - Déploiement WhatsApp

## 🚀 **ÉTAPES À EXÉCUTER MAINTENANT**

### **1. Installation des dépendances**
```bash
pip install python-dotenv requests flask
```

### **2. Configuration (IMPORTANT)**
```bash
# Ouvrir le fichier .env et remplacer par VOS vraies valeurs :
# ULTRAMSG_TOKEN=VOTRE_VRAI_TOKEN_ICI
# ULTRAMSG_INSTANCE_ID=VOTRE_VRAIE_INSTANCE_ICI
```

### **3. Entraîner le modèle Rasa**
```bash
rasa train
```

### **4. Démarrer le bot**
```bash
python run_ultramsg.py
```

### **5. Exposer avec ngrok (autre terminal)**
```bash
# Télécharger ngrok sur https://ngrok.com/download
ngrok http 5005
```

### **6. Configurer le webhook Ultramsg**
```
URL: https://VOTRE_URL_NGROK.ngrok.io/webhooks/ultramsg/webhook
Méthode: POST
```

### **7. Test rapide**
```bash
python test_ultramsg.py
```

## 📱 **TEST WHATSAPP**

**Envoyez ces messages sur WhatsApp :**
- "Bonjour" → Menu principal
- "E-carrière" → Services e-carrière  
- "PGDE" → Services PGDE
- "1" → Option 1 du menu

## 🔧 **Dépannage express**

### ❌ **Bot ne répond pas :**
1. Vérifier que `python run_ultramsg.py` fonctionne
2. Vérifier que ngrok affiche l'URL HTTPS
3. Vérifier le webhook dans Ultramsg dashboard
4. Regarder les logs dans la console

### ❌ **Erreur credentials :**
1. Ouvrir `.env`
2. Remplacer `ULTRAMSG_TOKEN` par votre vrai token
3. Remplacer `ULTRAMSG_INSTANCE_ID` par votre vraie instance
4. Redémarrer `python run_ultramsg.py`

### ❌ **Erreur modèle :**
```bash
rasa train
python run_ultramsg.py
```

## 🎉 **C'EST PRÊT !**

Votre chatbot Rasa fonctionne maintenant sur WhatsApp !

**Fichiers créés :**
- ✅ `ultramsg_connector.py` - Connecteur Ultramsg
- ✅ `run_ultramsg.py` - Script de démarrage
- ✅ `.env` - Configuration
- ✅ `test_ultramsg.py` - Tests
- ✅ Guides complets

**Prochaines étapes :**
- Personnaliser les réponses
- Ajouter des fonctionnalités
- Déployer en production