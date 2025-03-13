from typing import Any, Text, Dict, List
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class ActionAskHelp(Action):
    def name(self) -> Text:
        return "action_ask_help"

    def run(self, dispatcher, tracker, domain):
        buttons = [
            {"title": "Horaires", "payload": "/ask_hours"},
            {"title": "Créer un compte", "payload": "/ask_account_creation"},
            {"title": "Connexion", "payload": "/ask_login"},
            {"title": "Lien tutoriel", "payload": "/ask_tutorial_link"},
            {"title": "Postuler à la fonction publique", "payload": "/ask_public_service_application"}
        ]
        dispatcher.utter_message(text="Que souhaitez-vous savoir ?", buttons=buttons)
        return []
