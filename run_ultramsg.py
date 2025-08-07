#!/usr/bin/env python3
"""
🚀 Script de démarrage pour le chatbot Rasa avec Ultramsg WhatsApp
"""

import os
import sys
import logging
from typing import Dict, Any
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Ajouter le répertoire courant au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from rasa.core.agent import Agent
    from ultramsg_connector import UltramsgInput
    from flask import Flask
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print("💡 Installez les dépendances: pip install rasa flask requests python-dotenv")
    sys.exit(1)

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_agent(model_path: str = "models") -> Agent:
    """Charger le modèle Rasa le plus récent."""
    try:
        if os.path.isdir(model_path):
            models = [f for f in os.listdir(model_path) if f.endswith('.tar.gz')]
            if not models:
                raise FileNotFoundError("❌ Aucun modèle trouvé dans le répertoire models/")
            
            latest_model = os.path.join(model_path, sorted(models)[-1])
        else:
            latest_model = model_path
            
        logger.info(f"📦 Chargement du modèle: {latest_model}")
        
        # Charger avec les endpoints pour les actions personnalisées
        from rasa.core.utils import AvailableEndpoints
        endpoints_path = "endpoints.yml"
        
        if os.path.exists(endpoints_path):
            endpoints = AvailableEndpoints.read_endpoints(endpoints_path)
            agent = Agent.load(latest_model, action_endpoint=endpoints.action)
            logger.info("✅ Modèle chargé avec endpoints")
        else:
            agent = Agent.load(latest_model)
            logger.info("⚠️ Modèle chargé sans endpoints")
            
        logger.info("✅ Modèle chargé avec succès")
        return agent
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du chargement du modèle: {e}")
        sys.exit(1)

def setup_ultramsg_channel() -> UltramsgInput:
    """Configurer le canal Ultramsg."""
    
    # Récupérer les credentials depuis les variables d'environnement
    ultramsg_credentials = {
        "token": os.getenv("ULTRAMSG_TOKEN"),
        "instance_id": os.getenv("ULTRAMSG_INSTANCE_ID"),
        "verify_token": os.getenv("WEBHOOK_VERIFY_TOKEN", "mon_token_secret_123"),
        "webhook_url": "/webhooks/ultramsg/webhook"
    }
    
    # Vérifier que tous les credentials sont configurés
    missing_credentials = []
    for key, value in ultramsg_credentials.items():
        if not value or value == "":
            missing_credentials.append(key)
    
    if missing_credentials:
        logger.error(f"❌ Credentials manquants: {missing_credentials}")
        logger.error("💡 Vérifiez votre fichier .env")
        sys.exit(1)
    
    logger.info("✅ Credentials Ultramsg configurés")
    return UltramsgInput.from_credentials(ultramsg_credentials)

def create_app(agent: Agent, ultramsg_channel: UltramsgInput) -> Flask:
    """Créer l'application Flask."""
    app = Flask(__name__)
    
    # Fonction de traitement des messages
    async def handle_message(user_message):
        """Traiter les messages entrants."""
        try:
            responses = await agent.handle_message(user_message)
            logger.info(f"✅ Message traité pour {user_message.sender_id}")
            return responses
        except Exception as e:
            logger.error(f"❌ Erreur lors du traitement du message: {e}")
            return []
    
    # Enregistrer le blueprint Ultramsg
    ultramsg_blueprint = ultramsg_channel.blueprint(handle_message)
    app.register_blueprint(ultramsg_blueprint)
    
    # Routes de monitoring
    @app.route("/health")
    def health_check():
        return {
            "status": "healthy", 
            "service": "rasa-ultramsg-bot",
            "version": "1.0"
        }
    
    @app.route("/")
    def info():
        return {
            "service": "🤖 Rasa Ultramsg WhatsApp Bot",
            "status": "🟢 En cours d'exécution",
            "endpoints": {
                "health": "/health",
                "ultramsg_webhook": "/webhooks/ultramsg/webhook"
            },
            "guide": "Envoyez un message WhatsApp pour commencer!"
        }
    
    return app

def main():
    """Fonction principale."""
    print("🚀 Démarrage du chatbot Rasa avec Ultramsg WhatsApp...")
    print("=" * 60)
    
    try:
        # 1. Charger l'agent Rasa
        agent = load_agent()
        
        # 2. Configurer le canal Ultramsg
        ultramsg_channel = setup_ultramsg_channel()
        
        # 3. Créer l'application Flask
        app = create_app(agent, ultramsg_channel)
        
        # 4. Configuration du serveur
        port = int(os.getenv("PORT", 5005))
        debug_mode = os.getenv("DEBUG_MODE", "False").lower() == "true"
        
        print(f"🌐 Serveur démarré sur le port {port}")
        print(f"📱 Webhook Ultramsg: http://localhost:{port}/webhooks/ultramsg/webhook")
        print(f"🔍 Monitoring: http://localhost:{port}/health")
        
        if debug_mode:
            print("🐛 Mode debug activé")
            print("💡 Pour production, définir DEBUG_MODE=False dans .env")
        
        print("=" * 60)
        print("✅ Bot prêt à recevoir des messages WhatsApp!")
        print("💬 Envoyez 'Bonjour' sur WhatsApp pour commencer")
        
        # 5. Démarrer le serveur
        app.run(host="0.0.0.0", port=port, debug=debug_mode)
        
    except KeyboardInterrupt:
        logger.info("🛑 Arrêt du serveur par l'utilisateur")
    except Exception as e:
        logger.error(f"❌ Erreur critique: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()