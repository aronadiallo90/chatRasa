import os
import pdfplumber
import pyodbc
import ollama
import faiss
import numpy as np
import requests
from sentence_transformers import SentenceTransformer
from typing import Text, Dict, Any
import mysql.connector
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionRedirectPlatform(Action):
    def name(self) -> Text:
        return "action_redirect_platform"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        platform = tracker.get_slot("platform")

        if platform == "E-Carrière":
            dispatcher.utter_message(response="utter_E_carriere")
        elif platform == "PGDE":
            dispatcher.utter_message(response="utter_pgde_menu")
        else:
            dispatcher.utter_message(text="Je ne suis pas sûr de la plateforme que vous avez choisie. Pouvez-vous réessayer ?")
            dispatcher.utter_message(response="utter_greet_with_name")

        return []



# class ActionValidateName(Action):
#     def name(self) -> str:
#         return "action_validate_name"

#     async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
#         name = tracker.get_slot("nom")
#         file_path = os.path.join("data", "lookups", "nom.txt")  # Chemin local
#         # Pour production, utiliser : file_path = os.path.join("data", "nom.txt")
#         try:
#             with open(file_path, "r", encoding="utf-8") as f:
#                 valid_names = [line.strip() for line in f]
#             if name in valid_names:
#                 dispatcher.utter_message(text=f"Nom valide : {name}")
#                 return [SlotSet("nom", name)]
#             else:
#                 dispatcher.utter_message(text="Nom non reconnu, veuillez réessayer.")
#                 return [SlotSet("nom", None)]
#         except FileNotFoundError:
#             dispatcher.utter_message(text="Erreur : fichier nom.txt introuvable.")
#             return [SlotSet("nom", None)]

class ActionResetNom(Action):
    def name(self):
        return "action_reset_nom"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("nom", None)]
class ActionExplainAccountCreation(Action):
    def name(self) -> Text:
        return "action_explain_account_creation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        platform = tracker.get_slot("platform")

        if platform == "E-Carrière":
            dispatcher.utter_message(response="utter_ask_account_creation")
        elif platform == "PGDE":
            dispatcher.utter_message(response="utter_ask_pgde_account_creation")
        else:
            dispatcher.utter_message(response="utter_ask_account_creation")

        return []

class ActionExplainLogin(Action):
    def name(self) -> Text:
        return "action_explain_login"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        platform = tracker.get_slot("platform")

        if platform == "E-Carrière":
            dispatcher.utter_message(response="utter_ask_login")
        elif platform == "PGDE":
            dispatcher.utter_message(response="utter_ask_pgde_login")
        else:
            dispatcher.utter_message(response="utter_ask_login")

        return []

class ActionExplainPasswordReset(Action):
    def name(self) -> Text:
        return "action_explain_password_reset"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        platform = tracker.get_slot("platform")

        if platform == "E-Carrière":
            dispatcher.utter_message(response="utter_ask_password_reset")
        elif platform == "PGDE":
            dispatcher.utter_message(response="utter_ask_pgde_password_reset")
        else:
            dispatcher.utter_message(response="utter_ask_password_reset")

        return []

