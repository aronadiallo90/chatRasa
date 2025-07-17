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
from typing import Text, Dict, Any, List  # Ensure List is imported



class ActionRedirectPlatform(Action):
    def name(self) -> Text:
        return "action_redirect_platform"

    def run(self, dispatcher, tracker, domain):
        platform = tracker.get_slot("platform")

        if platform == "E-Carrière":
            dispatcher.utter_message(response="utter_E_carriere")
        elif platform == "PGDE":
            dispatcher.utter_message(response="utter_pgde_menu")
        else:
            # dispatcher.utter_message(response="utter_no_plateform_info")
            dispatcher.utter_message(text="Je ne suis pas sûr de la plateforme que vous avez choisie.Pouvez-vous réessayer ?")
             dispatcher.utter_message(response="utter_greet_with_name")

        return []

