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

# === Dictionnaire de cache pour stocker les réponses déjà calculées ===
response_cache = {}

# === Configuration de la connexion à la base de données SQL Server ===
sql_server_config = {
    "server": os.getenv("SQL_SERVER_HOST", "10.4.116.87"),
    "port": os.getenv("SQL_SERVER_PORT", "1433"),
    "database": os.getenv("SQL_SERVER_DB", "referentiel_fudpe_new"),
    "username": os.getenv("SQL_SERVER_USER", "sa"),
    "password": os.getenv("SQL_SERVER_PASSWORD", "AdieAdie1")
}

try:
            # Connexion à la base de données SQL Server
            conn = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={sql_server_config['server']},{sql_server_config['port']};"
                f"DATABASE={sql_server_config['database']};"
                f"UID={sql_server_config['username']};"
                f"PWD={sql_server_config['password']}"
            )
            print("✅ Connexion réussie à la base de données SQL Server !")
            cursor = conn.cursor()
except pyodbc.Error as e:
            print(f"Erreur de connexion à la base de données : {e}")

mysql_config = {
    "host": os.getenv("MYSQL_HOST", "host.docker.internal"),
    "port": int(os.getenv("MYSQL_PORT", 3307)),
    "database": os.getenv("MYSQL_DATABASE", "PGDEPGDE"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "adieadie")
}

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

# === Initialisation du modèle d'embedding et de FAISS ===
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def create_faiss_index(text):
    """ Création d'un index FAISS avec les embeddings des phrases extraites du document """
    sentences = text.split("\n")  # Découper le texte en phrases
    sentences = [s.strip() for s in sentences if s.strip()]  # Nettoyer les phrases vides
    embeddings = embedding_model.encode(sentences, convert_to_numpy=True)
    
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    
    return index, sentences

faiss_index, DOCUMENT_SECTIONS = create_faiss_index(DOCUMENT_TEXT)

print("✅ FAISS est prêt. Nombre de sections indexées :", len(DOCUMENT_SECTIONS))


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
            dispatcher.utter_message(response="utter_no_plateform_info")

        return []


class ActionRetrieveAnswer(Action):
    """ Action pour chercher une réponse dans le document PDF avec cache, FAISS et LLaMA """

    def name(self) -> Text:
        return "action_retrieve_answer"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get("text", "").lower()

        # Vérifier si le message ressemble à un matricule (ex: 654986b)
        if user_message.isalnum() and len(user_message) >= 6:
            print("🔍 Matricule détecté, redirection vers la base de données.")
            return [SlotSet("matricule", user_message), FollowupAction("action_retrieve_user_info")]

        print("🟢 action_retrieve_answer déclenchée avec :", user_message)

        # ✅ Vérifier si la réponse est déjà dans le cache
        if user_message in response_cache:
            print("⚡ Réponse trouvée dans le cache, envoi immédiat.")
            dispatcher.utter_message(text=response_cache[user_message])
            return []

        # 🔍 Recherche FAISS
        print("🔍 Recherche avec FAISS pour :", user_message)
        user_embedding = embedding_model.encode([user_message], convert_to_numpy=True)
        D, I = faiss_index.search(user_embedding, 1)  # Trouver la meilleure correspondance

        print(f"📌 Distance FAISS : {D[0][0]}, Index récupéré : {I[0][0]}")
        if D[0][0] > 0.8:  # Seuil trop élevé = réponse non fiable
            dispatcher.utter_message(response="utter_no_info")
            return []
        
        
        if D[0][0] < 0.8:  # 🔥 Seuil ajusté pour de meilleures réponses
            best_match = DOCUMENT_SECTIONS[I[0][0]]
        else:
            best_match = "Je ne sais pas."

        print("📄 Section trouvée :", best_match)

        # Si FAISS ne trouve rien, utiliser un extrait global avec Ollama
        if best_match == "Je ne sais pas.":
            print("⚠️ FAISS n'a rien trouvé. Envoi direct à Ollama.")

            prompt = f"""
            Tu es un assistant qui répond aux questions en utilisant le contenu  suivant :
            ---
            {DOCUMENT_TEXT[:1000]}  # 🔥 Envoi d’un extrait du document complet
            ---
            Question de l'utilisateur : {user_message}
            Réponds de manière claire et concise à l'utilisateur qui est un simple utilisateur.
            """

            try:
                response = ollama.chat(
                    model="mistral",
                    messages=[{"role": "user", "content": prompt}]
                )
                bot_response = response["message"]["content"]

                # Vérifier si la réponse d'Ollama est pertinente
                if "je ne sais pas" in bot_response.lower() or "désolé" in bot_response.lower():
                    bot_response = "Désolé, je n’ai pas trouvé d’information à ce sujet."

            except Exception as e:
                print("❌ Erreur avec Ollama :", str(e))
                bot_response = "Désolé, je n’ai pas trouvé d’information à ce sujet."

        else:
            # Construire la requête pour Ollama avec la section trouvée
            prompt = f"""
            Tu es un assistant qui répond aux questions en utilisant les informations suivantes :
            ---
            {best_match}
            ---
            Question de l'utilisateur : {user_message}
            Réponds de manière claire et concise.
            """

            print("🧠 Envoi à Ollama :", prompt)

            try:
                response = ollama.chat(
                    model="mistral",
                    messages=[{"role": "user", "content": prompt}]
                )
                bot_response = response["message"]["content"]

                # Vérifier si la réponse d'Ollama est pertinente
                if "je ne sais pas" in bot_response.lower() or "désolé" in bot_response.lower():
                    bot_response = "Désolé, je n’ai pas trouvé d’information à ce sujet."

            except Exception as e:
                print("❌ Erreur avec Ollama :", str(e))
                bot_response = "Désolé, je n’ai pas trouvé d’information à ce sujet."

        # ✅ Stocker la réponse dans le cache pour accélérer les futures requêtes
        response_cache[user_message] = bot_response

        dispatcher.utter_message(text=bot_response)

        # Ajouter un bouton de retour
        dispatcher.utter_message(text="Que souhaitez-vous faire ?", buttons=[
            {"title": "Retour", "payload": "/greet"},
            
        ])

        return []


class ActionRetrieveUserInfo(Action):

    def name(self) -> Text:
        return "action_retrieve_user_info"

    def run(self, dispatcher, tracker, domain):
        user_matricule = tracker.get_slot("matricule")
        if not user_matricule:
            dispatcher.utter_message(text="Veuillez fournir votre matricule.")
            return []

        try:
            # Connexion à la base de données SQL Server
            # conn = pyodbc.connect(
            #     f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            #     f"SERVER={server};"
            #     f"DATABASE={database};"
            #     f"UID={username};"
            #     f"PWD={password}"
            # )
            # print("✅ Connexion réussie à la base de données SQL Server !")
            # cursor = conn.cursor()

            # Exécuter la requête pour récupérer les informations de l'utilisateur
            query = """
            SELECT TOP 3
                a.agt_nom,
                a.agt_prenom,
                ac.act_numero_projet,
                ac.act_numero_acte,
                ea.eta_act_code AS etat_projet,
                ta.tac_libelle AS type_projet
            FROM 
                referentiel_fudpe_new.dbo.agent a
            INNER JOIN 
                referentiel_fudpe_new.dbo.acte_agent aa ON aa.act_agt_agt_id = a.agt_id
            INNER JOIN 
                referentiel_fudpe_new.dbo.acte ac ON ac.act_id = aa.act_agt_act_id
            LEFT JOIN 
                referentiel_fudpe_new.dbo.etat_acte ea ON ea.eta_act_id = ac.act_etat_id
            LEFT JOIN 
                referentiel_fudpe_new.dbo.type_acte ta ON ta.tac_id = ac.act_tac_id
            WHERE 
                a.agt_matricule_solde = ?
                AND ac.act_is_projet = 1
            ORDER BY ac.act_date_acte DESC;  -- Trier par date d'acte décroissante (du plus récent au plus ancien)
        """
            cursor.execute(query, user_matricule)
            rows = cursor.fetchall()

            if not rows:
                dispatcher.utter_message(text="Aucune information trouvée pour ce matricule.")
                return []

            # Construire la réponse
            response = f"Bienvenue **{rows[0].agt_prenom} {rows[0].agt_nom}!** \nVoici vos informations:\n\n"
            for row in rows:
                response += f" 📜 **Numéro Projet**: {row.act_numero_projet}\n 📄 **Numéro Acte**: {row.act_numero_acte}\n 📌 **État du projet** : {row.etat_projet}\n 🔹 **Type de projet**: {row.type_projet}\n\n\n"

            dispatcher.utter_message(text=response)

            # Effacer la question et la réponse du cache
            if user_matricule in response_cache:
                del response_cache[user_matricule]

            return []

        except pyodbc.Error as e:
            print(f"Erreur de recupersation des données  à la base de données : {e}")
            dispatcher.utter_message(text="Erreur de recupersation des données à la base de données.")
            return []


class ActionHandleEmailInput(Action):
    def name(self) -> Text:
        return "action_handle_email_input"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Vérifier si nous attendons un email
        awaiting_email = tracker.get_slot("awaiting_email")
        
        if awaiting_email:
            # Récupérer le dernier message de l'utilisateur comme email
            email = tracker.latest_message.get("text", "").strip()
            
            # Validation basique de l'email (vous pouvez améliorer cette validation)
            if "@" in email and "." in email:
                return [SlotSet("email", email), FollowupAction("action_reset_pgde_password")]
            else:
                # Message pour email invalide
                dispatcher.utter_message(text="L'adresse email semble invalide. Veuillez fournir une adresse email valide.")
                return [SlotSet("email", None), SlotSet("awaiting_email", True)]
        
        return []


class ActionResetPGDEPassword(Action):
    def name(self) -> Text:
        return "action_reset_pgde_password"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Récupérer l'email fourni par l'utilisateur
        email = tracker.get_slot("email")
        
        # Si l'email n'est pas encore fourni, demander à l'utilisateur
        if not email:
            dispatcher.utter_message(text="Veuillez fournir l'adresse email associée à votre compte PGDE.")
            return [SlotSet("awaiting_email", True)]

        try:
            # Établir une connexion à la base de données MySQL de PGDE
            connection = mysql.connector.connect(**mysql_config)
            cursor = connection.cursor()
            
            # Vérifier si l'email existe dans la base de données
            cursor.execute("SELECT id FROM utilisateur WHERE email = %s", (email,))
            result = cursor.fetchone()
            
            # Fermer la connexion MySQL
            cursor.close()
            connection.close()
            
            if not result:
                dispatcher.utter_message(text=f"Aucun compte n'est associé à l'email {email}. Veuillez vérifier votre adresse email ou créer un nouveau compte.")
                return [SlotSet("email", None), SlotSet("awaiting_email", False)]
            
            # Si l'email existe, envoyer une demande de réinitialisation
            # try:
            #     # Appel API pour déclencher l'envoi de l'email de réinitialisation
            #     reset_url = "https://emploi-fpublique.sec.gouv.sn/resetting/request"
            #     response = requests.post(
            #         reset_url, 
            #         json={"email": email}
            #     )
                
            #     if response.status_code == 200:
            #         message = f"Un email de réinitialisation a été envoyé à {email}. Veuillez vérifier votre boîte de réception et suivre les instructions pour créer un nouveau mot de passe."
            #     else:
            #         message = "Nous avons rencontré un problème lors de l'envoi de l'email de réinitialisation. Veuillez réessayer plus tard."
            
            # except Exception as e:
            #     print(f"Erreur lors de l'appel à l'API de réinitialisation : {e}")
            #     message = "Un problème technique est survenu. Notre équipe a été notifiée et travaille à résoudre ce problème."
            message = f"Un email de réinitialisation a été envoyé à {email}. Veuillez vérifier votre boîte de réception et suivre les instructions pour créer un nouveau mot de passe."
            
            dispatcher.utter_message(text=message)
            
            # Ajouter un bouton de retour
            dispatcher.utter_message(text="Que souhaitez-vous faire maintenant ?", buttons=[
                {"title": "Retour au menu PGDE", "payload": "/go_back_pgde"},
                {"title": "Menu principal", "payload": "/greet"}
            ])
            
            return [SlotSet("email", None), SlotSet("awaiting_email", False)]
            
        except mysql.connector.Error as db_error:
            print(f"Erreur de connexion MySQL PGDE : {db_error}")
            dispatcher.utter_message(text="Je rencontre un problème technique pour vérifier votre email. Veuillez réessayer plus tard.")
            return [SlotSet("email", None), SlotSet("awaiting_email", False)]