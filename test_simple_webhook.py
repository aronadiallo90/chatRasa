#!/usr/bin/env python3
"""
🧪 Test du serveur simple
"""

import requests
import json

def test_simple_server():
    """Tester le serveur simple"""
    
    webhook_url = "http://localhost:5007/webhooks/ultramsg/webhook"
    
    # Format exact de Ultramsg
    ultramsg_data = {
        "event_type": "message_received",
        "instanceId": "40778",
        "data": {
            "id": "test_id",
            "from": "221776791039@c.us",
            "to": "221767914708@c.us",
            "type": "chat",
            "body": "Bonjour",
            "pushname": "Test Bot",
            "time": 1754570000
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("🧪 Test serveur simple...")
        print(f"📨 Envoi vers: {webhook_url}")
        
        response = requests.post(webhook_url, json=ultramsg_data, headers=headers)
        
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Réponse: {response.text}")
        
        if response.status_code == 200:
            print("🎉 Le serveur simple fonctionne !")
        else:
            print("❌ Problème avec le serveur simple")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_simple_server()