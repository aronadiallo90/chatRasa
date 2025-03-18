import os
import pdfplumber
import ollama
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import Text, Dict, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted

# === Dictionnaire de cache pour stocker les réponses déjà calculées ===
response_cache = {}

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

class ActionRetrieveAnswer(Action):
    """ Action pour chercher une réponse dans le document PDF avec cache, FAISS et LLaMA """

    def name(self) -> Text:
        return "action_retrieve_answer"

    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get("text", "").lower()
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
        
        if D[0][0] < 0.8:  # 🔥 Seuil ajusté pour de meilleures réponses
            best_match = DOCUMENT_SECTIONS[I[0][0]]
        else:
            best_match = "Je ne sais pas."

        print("📄 Section trouvée :", best_match)

        # Si FAISS ne trouve rien, utiliser un extrait global avec Ollama
        if best_match == "Je ne sais pas.":
            print("⚠️ FAISS n'a rien trouvé. Envoi direct à Ollama.")

            prompt = f"""
            Tu es un assistant qui répond aux questions en utilisant le document suivant :
            ---
            {DOCUMENT_TEXT[:1000]}  # 🔥 Envoi d’un extrait du document complet
            ---
            Question de l'utilisateur : {user_message}
            Réponds de manière claire et concise.
            """

            try:
                response = ollama.chat(
                    model="mistral",
                    messages=[{"role": "user", "content": prompt}]
                )
                bot_response = response["message"]["content"]

            except Exception as e:
                print("❌ Erreur avec Ollama :", str(e))
                bot_response = "Désolé, une erreur est survenue lors de la recherche."

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

            except Exception as e:
                print("❌ Erreur avec Ollama :", str(e))
                bot_response = "Désolé, une erreur est survenue lors de la recherche."

        # ✅ Stocker la réponse dans le cache pour accélérer les futures requêtes
        response_cache[user_message] = bot_response

        dispatcher.utter_message(text=bot_response)

        # Ajouter un bouton de retour
        dispatcher.utter_message(text="Que souhaitez-vous faire ?", buttons=[
            {"title": "Retour", "payload": "/go_back"},
            {"title": "Obtenir de l'aide", "payload": "/ask_help"}
        ])

        return []
