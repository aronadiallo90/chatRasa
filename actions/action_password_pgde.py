from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import mysql.connector

class ActionPgdeHandleForgottenPassword(Action):
    def name(self):
        return "action_pgde_handle_forgotten_password" 

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        email = tracker.get_slot("user_email")

        if not email:
            dispatcher.utter_message(text="Veuillez fournir votre adresse e-mail.")
            return []

        try:
            connection = mysql.connector.connect(
                host="10.121.220.44",
                port=3306,
                database="PGDEPGDE",  # à adapter
                user="root",  # à adapter
                password="adieadie"  # à adapter
            )
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM utilisateur WHERE email = %s", (email,))
            result = cursor.fetchone()

            if result:
                dispatcher.utter_message(text="Un lien de réinitialisation vous a été envoyé par e-mail.")
                # Tu peux ajouter ici un appel à une API d'envoi d'e-mail ou autre action
            else:
                dispatcher.utter_message(text="Cette adresse e-mail n’est pas enregistrée dans notre base.")

        except Exception as e:
            print(f"Erreur MySQL: {e}")
            dispatcher.utter_message(text="Erreur lors de la connexion à la base de données.")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        return []
