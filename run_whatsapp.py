#!/usr/bin/env python3
"""
Script de démarrage pour le chatbot Rasa avec intégration WhatsApp
"""

import os
import sys
import logging
from typing import Dict, Any

# Ajouter le répertoire courant au path pour importer le connecteur
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rasa.core.agent import Agent
from rasa.core.utils import configure_file_logging
from whatsapp_connector import WhatsAppInput

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_agent(model_path: str = "models") -> Agent:
    """Charge le modèle Rasa."""
    try:
        # Trouver le modèle le plus récent
        if os.path.isdir(model_path):
            models = [f for f in os.listdir(model_path) if f.endswith('.tar.gz')]
            if not models:
                raise FileNotFoundError("Aucun modèle trouvé dans le répertoire models/")
            latest_model = os.path.join(model_path, sorted(models)[-1])
        else:
            latest_model = model_path
            
        logger.info(f"Chargement du modèle : {latest_model}")
        agent = Agent.load(latest_model)
        return agent
    except Exception as e:
        logger.error(f"Erreur lors du chargement du modèle : {e}")
        sys.exit(1)

def setup_whatsapp_channel() -> WhatsAppInput:
    """Configure le canal WhatsApp."""
    # Configuration WhatsApp (remplacez par vos vraies valeurs)
    whatsapp_credentials = {
        "access_token": os.getenv("WHATSAPP_ACCESS_TOKEN", "YOUR_WHATSAPP_ACCESS_TOKEN"),
        "phone_number_id": os.getenv("WHATSAPP_PHONE_NUMBER_ID", "YOUR_PHONE_NUMBER_ID"),
        "verify_token": os.getenv("WHATSAPP_VERIFY_TOKEN", "YOUR_VERIFY_TOKEN"),
        "webhook_url": "/webhooks/whatsapp/webhook"
    }
    
    # Vérifier que les credentials sont configurés
    for key, value in whatsapp_credentials.items():
        if value.startswith("YOUR_"):
            logger.warning(f"⚠️  {key} n'est pas configuré dans credentials.yml ou variables d'environnement")
    
    return WhatsAppInput.from_credentials(whatsapp_credentials)

def main():
    """Fonction principale."""
    logger.info("🚀 Démarrage du chatbot Rasa avec WhatsApp...")
    
    # Charger l'agent Rasa
    agent = load_agent()
    
    # Configurer le canal WhatsApp
    whatsapp_channel = setup_whatsapp_channel()
    
    # Créer l'application Flask pour les webhooks
    from flask import Flask
    app = Flask(__name__)
    
    # Fonction de traitement des messages
    def handle_message(user_message):
        """Traite les messages entrants."""
        try:
            response = agent.handle_message(user_message)
            logger.info(f"Message traité pour {user_message.sender_id}")
            return response
        except Exception as e:
            logger.error(f"Erreur lors du traitement du message : {e}")
    
    # Enregistrer le blueprint WhatsApp
    whatsapp_blueprint = whatsapp_channel.blueprint(handle_message)
    app.register_blueprint(whatsapp_blueprint, url_prefix="/webhooks/whatsapp")
    
    # Route de santé
    @app.route("/health")
    def health_check():
        return {"status": "healthy", "service": "rasa-whatsapp-bot"}
    
    # Route d'information
    @app.route("/")
    def info():
        return {
            "service": "Rasa WhatsApp Bot",
            "status": "running",
            "endpoints": {
                "health": "/health",
                "whatsapp_webhook": "/webhooks/whatsapp/webhook"
            }
        }
    
    # Démarrer le serveur
    port = int(os.getenv("PORT", 5005))
    logger.info(f"🌐 Serveur démarré sur le port {port}")
    logger.info("📱 Canal WhatsApp configuré sur /webhooks/whatsapp/webhook")
    logger.info("🔗 Pour tester localement, utilisez ngrok : ngrok http 5005")
    
    app.run(host="0.0.0.0", port=port, debug=False)

if __name__ == "__main__":
    main()