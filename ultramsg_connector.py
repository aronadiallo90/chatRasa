import logging
import json
import requests
import os
from typing import Dict, Text, Any, List, Optional
from flask import Flask, request, jsonify
from dotenv import load_dotenv

from rasa.core.channels.channel import InputChannel, UserMessage, OutputChannel

# Charger les variables d'environnement
load_dotenv()

logger = logging.getLogger(__name__)

class UltramsgOutput(OutputChannel):
    """Canal de sortie pour Ultramsg WhatsApp."""

    def __init__(self, token: Text, instance_id: Text) -> None:
        self.token = token
        self.instance_id = instance_id
        self.base_url = f"{os.getenv('ULTRAMSG_BASE_URL', 'https://api.ultramsg.com')}/{instance_id}/messages"

    async def send_text_message(
        self, recipient_id: Text, text: Text, **kwargs: Any
    ) -> None:
        """Envoyer un message texte via Ultramsg."""
        
        # Préparer les données comme dans votre code Java
        data = {
            'token': self.token,
            'to': f"+{recipient_id.replace('+', '')}",
            'body': text,
            'priority': '1',
            'referenceId': ''
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            response = requests.post(f"{self.base_url}/chat", data=data, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            if result.get('sent'):
                logger.info(f"✅ Message envoyé avec succès à {recipient_id}")
            else:
                logger.error(f"❌ Échec envoi message à {recipient_id}: {result}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erreur réseau lors de l'envoi à {recipient_id}: {e}")
        except Exception as e:
            logger.error(f"❌ Erreur inattendue lors de l'envoi à {recipient_id}: {e}")

    async def send_text_with_buttons(
        self,
        recipient_id: Text,
        text: Text,
        buttons: List[Dict[Text, Any]],
        **kwargs: Any,
    ) -> None:
        """Envoyer un message avec boutons (simulés par numérotation)."""
        
        # Ultramsg ne supporte pas les boutons natifs, on utilise une liste numérotée
        message_with_options = f"{text}\n\n"
        for i, button in enumerate(buttons, 1):
            title = button.get("title", f"Option {i}")
            message_with_options += f"{i}. {title}\n"
        
        message_with_options += "\n💡 *Tapez le numéro de votre choix*"
        
        await self.send_text_message(recipient_id, message_with_options)

class UltramsgInput(InputChannel):
    """Canal d'entrée pour Ultramsg WhatsApp."""

    @classmethod
    def name(cls) -> Text:
        return "ultramsg"

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> InputChannel:
        if not credentials:
            cls.raise_missing_credentials_exception()

        return cls(
            token=credentials.get("token"),
            instance_id=credentials.get("instance_id"),
            verify_token=credentials.get("verify_token"),
            webhook_url=credentials.get("webhook_url", "/webhooks/ultramsg/webhook")
        )

    def __init__(
        self,
        token: Text,
        instance_id: Text,
        verify_token: Text,
        webhook_url: Text = "/webhooks/ultramsg/webhook"
    ) -> None:
        self.token = token
        self.instance_id = instance_id
        self.verify_token = verify_token
        self.webhook_url = webhook_url

    def get_output_channel(self) -> OutputChannel:
        return UltramsgOutput(self.token, self.instance_id)

    def blueprint(self, on_new_message):
        from flask import Blueprint
        ultramsg_webhook = Blueprint("ultramsg_webhook", __name__)

        @ultramsg_webhook.route("/webhooks/ultramsg/", methods=["GET"])
        def health():
            return jsonify({
                "status": "Ultramsg webhook actif", 
                "service": "rasa-ultramsg-connector"
            })

        @ultramsg_webhook.route("/webhooks/ultramsg/webhook", methods=["GET"])
        def verify():
            """Vérification du webhook Ultramsg."""
            verify_token = request.args.get("verify_token")
            
            if verify_token == self.verify_token:
                logger.info("✅ Webhook Ultramsg vérifié avec succès")
                return jsonify({"status": "verified"})
            else:
                logger.error("❌ Échec de la vérification du webhook Ultramsg")
                return jsonify({"error": "Token de vérification invalide"}), 403

        @ultramsg_webhook.route("/webhooks/ultramsg/webhook", methods=["POST"])
        def webhook():
            """Traiter les messages WhatsApp entrants via Ultramsg."""
            try:
                data = request.get_json() or request.form.to_dict()
                logger.info(f"📨 Données webhook reçues: {data}")
                
                # Format Ultramsg réel: {'event_type': 'message_received', 'data': {...}}
                if data.get("event_type") == "message_received" and "data" in data:
                    message_data = data["data"]
                    sender_id = message_data.get("from", "").replace("@c.us", "").replace("+", "")
                    message_body = message_data.get("body", "")
                    message_type = message_data.get("type", "text")
                    
                    # Traiter seulement les messages texte/chat
                    if message_type in ["text", "chat"] and message_body.strip():
                        logger.info(f"🔄 Traitement: {sender_id} -> {message_body}")
                        self._handle_user_message(message_body, sender_id, on_new_message)
                    else:
                        logger.info(f"ℹ️ Type de message ignoré: {message_type}")
                
                # Format simple pour les tests (garder pour compatibilité)
                elif "from" in data and "body" in data:
                    sender_id = data["from"].replace("+", "")
                    message_body = data["body"]
                    message_type = data.get("type", "text")
                    
                    if message_type in ["text", "chat"]:
                        self._handle_user_message(message_body, sender_id, on_new_message)
                
                return jsonify({"status": "success"})
            
            except Exception as e:
                logger.error(f"❌ Erreur lors du traitement du webhook: {e}")
                return jsonify({"status": "error", "message": str(e)}), 500

        return ultramsg_webhook

    def _handle_user_message(self, text: Text, sender_id: Text, on_new_message):
        """Traiter le message utilisateur entrant."""
        try:
            import asyncio
            
            # Traitement spécial pour les réponses numériques (boutons simulés)
            processed_text = self._process_numeric_response(text)
            
            output_channel = self.get_output_channel()
            user_msg = UserMessage(
                text=processed_text,
                output_channel=output_channel,
                sender_id=sender_id,
                input_channel=self.name()
            )
            
            # Exécuter la fonction async dans un nouveau loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(on_new_message(user_msg))
            finally:
                loop.close()
                
            logger.info(f"✅ Message traité de {sender_id}: {processed_text}")
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du traitement du message: {e}")

    def _process_numeric_response(self, text: Text) -> Text:
        """Convertir les réponses numériques en intents Rasa SANS mapping fixe."""
        text = text.strip()
        
        # NE PAS faire de mapping automatique - laisser Rasa gérer
        # Rasa va traiter le "1" selon le contexte de la conversation
        
        logger.info(f"📝 Message reçu: '{text}' (pas de conversion numérique)")
        return text