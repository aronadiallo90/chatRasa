#!/usr/bin/env python3
"""
🧪 Test d'envoi de message depuis le bot vers WhatsApp
"""

import requests
from dotenv import load_dotenv
import os

load_dotenv()

def send_test_message():
    """Envoyer un message de test via Ultramsg"""
    
    token = os.getenv("ULTRAMSG_TOKEN")
    instance_id = os.getenv("ULTRAMSG_INSTANCE_ID")
    
    # Votre numéro de téléphone (remplacez par le vôtre)
    your_phone = "+221776791039"  # Remplacez par VOTRE numéro
    
    url = f"https://api.ultramsg.com/{instance_id}/messages/chat"
    
    data = {
        'token': token,
        'to': your_phone,
        'body': '🤖 Test du bot Rasa ! Si vous recevez ce message, l\'envoi fonctionne.',
        'priority': '1'
    }
    
    try:
        print(f"📱 Envoi de message test vers {your_phone}...")
        response = requests.post(url, data=data)
        result = response.json()
        
        if result.get('sent'):
            print("✅ Message envoyé avec succès !")
            print(f"📄 Détails: {result}")
        else:
            print("❌ Échec envoi:")
            print(f"📄 Erreur: {result}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    send_test_message()