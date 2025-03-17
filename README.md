"# chatRasa" 
"# chatRasa" 

-pour entrainer le modele

-pour lancer l'api rasa
rasa run -m models --enable-api --cors "*" --debug


-pour actier les acrions et permettre une recherche intelligente 

rasa run actions --debug


curl -X POST http://localhost:11434/api/generate -d '{"model":"mistral","prompt":"À qui est destinée la plateforme E-Carrière ?"}'
# 🤖 Chatbot Rasa avec Ollama & FAISS

Ce projet est un chatbot intelligent basé sur **Rasa**, utilisant **FAISS** pour la recherche vectorielle et **Ollama** avec **Mistral/LLaMA3** pour générer des réponses à partir de documents PDF.

## 🚀 **Installation et Lancement**
Suivez ces étapes pour configurer et exécuter le chatbot sur votre machine.

---

## 1️⃣ **Pré-requis**
Avant de commencer, assurez-vous d'avoir installé :
- [Python 3.8+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [Rasa](https://rasa.com/docs/rasa/installation)
- [Ollama](https://ollama.com/download)

---

## 2️⃣ **Téléchargement du Projet**
Clonez le dépôt Git sur votre machine :
```sh
git clone https://github.com/ton-utilisateur/ton-repo.git
cd ton-repo
```

---

## 3️⃣ **Création et Activation de l’Environnement Virtuel**
Créez un environnement virtuel pour isoler les dépendances :
```sh
python -m venv .venv
source .venv/bin/activate   # Sur macOS/Linux
.\.venv\Scripts\activate    # Sur Windows
```

---

## 4️⃣ **Installation des Dépendances**
Installez les packages nécessaires :
```sh
pip install -r requirements.txt
```

---

## 5️⃣ **Téléchargement du Modèle LLM**
Avant de lancer le chatbot, assurez-vous d’avoir téléchargé **Mistral** ou **LLaMA3** :
```sh
ollama pull mistral
# ou
#ollama pull llama3
```

Testez si Ollama fonctionne :
```sh
ollama run mistral "Bonjour, peux-tu répondre à une question ?"
```

---

## 6️⃣ **Lancement du Chatbot**
### 🔹 **1. Entraîner le modèle Rasa**
Avant de l'exécuter, entraînez le modèle :
```sh
rasa train
```

### 🔹 **2. Démarrer le serveur Rasa**
Lancez Rasa pour qu'il puisse traiter les messages :
```sh
rasa run --enable-api --debug
```

### 🔹 **3. Démarrer le serveur d’actions personnalisées**
Dans un autre terminal, lancez le serveur d’actions :
```sh
rasa run actions --debug
```

---

## 7️⃣ **Utilisation**
Une fois lancé, le chatbot peut être utilisé via :
- **L’interface web** (si un front est intégré)
- **Postman** (ou n’importe quel client API) via :
  ```sh
  curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{"sender": "test_user", "message": "Bonjour"}'
  ```
- **Le mode interactif Rasa** :
  ```sh
  rasa shell
  ```

---

## 8️⃣ **Problèmes Courants & Solutions**
### ❌ *Problème : "ollama command not found"*
🔎 Assurez-vous que Ollama est bien installé :
```sh
ollama list
```
### ❌ *Problème : "ollama n'est pas lancé"*
🔎 Assurez-vous que Ollama est bien lancer :
```sh
ollama serve
```


Si aucun modèle n’apparaît, installez **Mistral** ou **LLaMA3**.

### ❌ *Problème : Rasa ne trouve pas l’action `action_retrieve_answer`*
🔎 Relancez le serveur d’actions avec :
```sh
rasa run actions --debug
```

---

## 👐 **Fichiers Clés**
- `domain.yml` → Définit les intentions, réponses et actions du bot.
- `nlu.yml` → Contient les exemples d’entraînement pour la classification d’intents.
- `stories.yml` → Définit les conversations et scénarios possibles.
- `actions.py` → Implémente l’intégration avec FAISS et Ollama.
- `config.yml` → Paramètres de pipeline et politiques de Rasa.
- `data/knowledge_base/faq.pdf` → Le document utilisé pour la recherche de réponses.

---






 
