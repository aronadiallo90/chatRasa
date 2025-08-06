import logging
import json
import requests
from typing import Dict, Text, Any, List, Optional
from flask import Flask, request, jsonify

from rasa.core.channels.channel import InputChannel, UserMessage, OutputChannel
from rasa.core.channels.channel import CollectingOutputChannel

logger = logging.getLogger(__name__)


class WhatsAppOutput(OutputChannel):
    """Output channel for WhatsApp."""

    def __init__(self, access_token: Text, phone_number_id: Text) -> None:
        self.access_token = access_token
        self.phone_number_id = phone_number_id
        self.base_url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"

    async def send_text_message(
        self, recipient_id: Text, text: Text, **kwargs: Any
    ) -> None:
        """Send a text message to WhatsApp."""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "text",
            "text": {"body": text}
        }
        
        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            logger.info(f"Message sent successfully to {recipient_id}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send message to {recipient_id}: {e}")

    async def send_text_with_buttons(
        self,
        recipient_id: Text,
        text: Text,
        buttons: List[Dict[Text, Any]],
        **kwargs: Any,
    ) -> None:
        """Send a text message with interactive buttons."""
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # Convert Rasa buttons to WhatsApp format
        interactive_buttons = []
        for i, button in enumerate(buttons[:3]):  # WhatsApp limits to 3 buttons
            interactive_buttons.append({
                "type": "reply",
                "reply": {
                    "id": f"btn_{i}",
                    "title": button.get("title", "Option")[:20]  # Max 20 chars
                }
            })
        
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": text},
                "action": {"buttons": interactive_buttons}
            }
        }
        
        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            logger.info(f"Interactive message sent successfully to {recipient_id}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send interactive message to {recipient_id}: {e}")


class WhatsAppInput(InputChannel):
    """WhatsApp input channel implementation."""

    @classmethod
    def name(cls) -> Text:
        return "whatsapp"

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> InputChannel:
        if not credentials:
            cls.raise_missing_credentials_exception()

        return cls(
            access_token=credentials.get("access_token"),
            phone_number_id=credentials.get("phone_number_id"),
            verify_token=credentials.get("verify_token"),
            webhook_url=credentials.get("webhook_url", "/webhooks/whatsapp/webhook")
        )

    def __init__(
        self,
        access_token: Text,
        phone_number_id: Text,
        verify_token: Text,
        webhook_url: Text = "/webhooks/whatsapp/webhook"
    ) -> None:
        self.access_token = access_token
        self.phone_number_id = phone_number_id
        self.verify_token = verify_token
        self.webhook_url = webhook_url

    def get_output_channel(self) -> OutputChannel:
        return WhatsAppOutput(self.access_token, self.phone_number_id)

    def blueprint(self, on_new_message) -> Flask:
        whatsapp_webhook = Flask(__name__)

        @whatsapp_webhook.route("/", methods=["GET"])
        def health():
            return jsonify({"status": "WhatsApp webhook is running"})

        @whatsapp_webhook.route(self.webhook_url, methods=["GET"])
        def verify():
            """Webhook verification for WhatsApp."""
            verify_token = request.args.get("hub.verify_token")
            challenge = request.args.get("hub.challenge")
            
            if verify_token == self.verify_token:
                logger.info("WhatsApp webhook verified successfully")
                return challenge
            else:
                logger.error("WhatsApp webhook verification failed")
                return "Verification failed", 403

        @whatsapp_webhook.route(self.webhook_url, methods=["POST"])
        def webhook():
            """Handle incoming WhatsApp messages."""
            try:
                data = request.get_json()
                logger.info(f"Received webhook data: {data}")
                
                if not data or "entry" not in data:
                    return jsonify({"status": "ok"})
                
                for entry in data["entry"]:
                    changes = entry.get("changes", [])
                    for change in changes:
                        value = change.get("value", {})
                        messages = value.get("messages", [])
                        
                        for message in messages:
                            sender_id = message.get("from")
                            message_type = message.get("type")
                            
                            if message_type == "text":
                                text = message.get("text", {}).get("body", "")
                                self._handle_user_message(text, sender_id, on_new_message)
                            
                            elif message_type == "interactive":
                                # Handle button clicks
                                interactive = message.get("interactive", {})
                                button_reply = interactive.get("button_reply", {})
                                payload = button_reply.get("id", "")
                                title = button_reply.get("title", "")
                                
                                # Use title as message text for Rasa
                                self._handle_user_message(title, sender_id, on_new_message)
                
                return jsonify({"status": "ok"})
            
            except Exception as e:
                logger.error(f"Error processing WhatsApp webhook: {e}")
                return jsonify({"status": "error", "message": str(e)}), 500

        return whatsapp_webhook

    def _handle_user_message(self, text: Text, sender_id: Text, on_new_message):
        """Process incoming user message."""
        try:
            output_channel = self.get_output_channel()
            user_msg = UserMessage(
                text=text,
                output_channel=output_channel,
                sender_id=sender_id,
                input_channel=self.name()
            )
            on_new_message(user_msg)
            logger.info(f"Processed message from {sender_id}: {text}")
        except Exception as e:
            logger.error(f"Error handling user message: {e}")