#!/usr/bin/env python3
"""
🧪 Test final du webhook Ultramsg
"""

import requests
import json

def test_webhook():
    """Simuler un message WhatsApp"""
    url = "https://silver-queens-cut.loca.lt/webhooks/ultramsg/webhook"
    headers = {
        "bypass-tunnel-reminder": "true",
        "Content-Type": "application/json"
    }
    
    # Message de test
    test_data = {
        "from": "212600000000",
        "body": "Bonjour test",
        "type": "text",
        "id": "test_123"
    }
    
    try:
        print("🧪 Test du webhook avec message simulé...")
        response = requests.post(url, json=test_data, headers=headers)
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Réponse: {response.text}")
        
        if response.status_code == 200:
            print("🎉 Webhook fonctionne ! Votre bot est prêt !")
        else:
            print("⚠️ Vérifiez les logs du serveur")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_webhook()