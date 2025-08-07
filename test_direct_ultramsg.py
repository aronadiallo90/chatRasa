#!/usr/bin/env python3
"""
🧪 Test direct avec simulation de message Ultramsg
"""

import requests
import json

def test_direct_message():
    """Simuler directement un message comme Ultramsg l'envoie"""
    
    webhook_url = "https://monbot123.loca.lt/webhooks/ultramsg/webhook"
    
    # Format exact de Ultramsg (basé sur vos logs)
    ultramsg_data = {
        "event_type": "message_received",
        "instanceId": "40778",
        "data": {
            "id": "test_id",
            "from": "221776791039@c.us",  # Votre numéro
            "to": "221767914708@c.us",
            "type": "chat",
            "body": "Bonjour",
            "pushname": "Test Bot",
            "time": 1754570000
        }
    }
    
    headers = {
        "bypass-tunnel-reminder": "true",
        "Content-Type": "application/json"
    }
    
    try:
        print("🧪 Test direct du webhook avec format Ultramsg...")
        print(f"📨 Envoi vers: {webhook_url}")
        print(f"📄 Données: {json.dumps(ultramsg_data, indent=2)}")
        
        response = requests.post(webhook_url, json=ultramsg_data, headers=headers)
        
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Réponse: {response.text}")
        
        if response.status_code == 200:
            print("🎉 Le webhook fonctionne ! Vérifiez les logs du serveur.")
        else:
            print("❌ Problème avec le webhook")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_direct_message()