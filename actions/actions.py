import os
import pdfplumber
import ollama  # Importer Ollama pour utiliser LLaMA
from typing import Text, List, Dict, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted

# === Chargement du document PDF ===
DOCUMENT_PATH = "data/knowledge_base/faq.pdf"

def extract_text_from_pdf(pdf_path):
    """ Extraction du texte depuis un PDF """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    return text

DOCUMENT_TEXT = extract_text_from_pdf(DOCUMENT_PATH)

class ActionAskHelp(Action):
    """ Action pour guider l'utilisateur avec des boutons """
    
    def name(self) -> str:
        return "action_ask_help"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        buttons = [
            {"title": "Horaires", "payload": "/ask_hours"},
            {"title": "Créer un compte", "payload": "/ask_account_creation"},
            {"title": "Connexion", "payload": "/ask_login"},
            {"title": "Lien tutoriel", "payload": "/ask_tutorial_link"},
            {"title": "Postuler à la fonction publique", "payload": "/ask_public_service_application"}
        ]
        dispatcher.utter_message(text="Que souhaitez-vous savoir ?", buttons=buttons)
        return []

class ActionRetrieveAnswer(Action):
    """ Action pour chercher une réponse dans le document PDF en utilisant LLaMA avec Ollama """
    
    def name(self) -> Text:
        return "action_retrieve_answer"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get("text", "").lower()
        entities = tracker.latest_message.get("entities", [])

        # Vérifier si une entité "service" est présente
        service = next((e["value"] for e in entities if e["entity"] == "service"), None)

        # Réponses prédéfinies
        predefined_answers = {
            "horaires": "Nos horaires sont du lundi au vendredi de 9h à 17h.",
            "créer un compte": "Rendez-vous sur notre site et cliquez sur 'Inscription'.",
            "connexion": "Utilisez vos identifiants pour vous connecter.",
            "lien tutoriel": "Voici le tutoriel : [Lien du tutoriel]",
            "postuler à la fonction publique": "Le processus d'inscription est détaillé sur notre site."
        }

        # Si la question est déjà connue, retourner la réponse directement
        for key, answer in predefined_answers.items():
            if key in user_message:
                dispatcher.utter_message(text=answer)
                return [UserUtteranceReverted()]

        # Sinon, recherche dans le document via LLaMA
        prompt = f"""
        Tu es un assistant qui répond aux questions des utilisateurs en utilisant le document suivant :
        ---
        {DOCUMENT_TEXT}
        ---
        Question de l'utilisateur : {user_message}
        Réponds de manière claire et précise en fonction du document.
        """

        print("🔍 Recherche dans LLaMA...")
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )

        bot_response = response["message"]["content"]

        # Vérifier si LLaMA a trouvé une réponse
        if not bot_response or len(bot_response) < 5:
            bot_response = "Je suis désolé, je ne connais pas la réponse à cette question."

        dispatcher.utter_message(text=bot_response)

        # Ajouter un bouton de retour
        dispatcher.utter_message(text="Que souhaitez-vous faire ?", buttons=[
            {"title": "Retour", "payload": "/go_back"},
            {"title": "Obtenir de l'aide", "payload": "/ask_help"}

        ])

        return [UserUtteranceReverted()]
