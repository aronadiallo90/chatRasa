#!/usr/bin/env python3
"""
🧪 Script de test pour l'intégration Ultramsg
"""

import os
import requests
import json
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def test_ultramsg_api():
    """Tester l'API Ultramsg directement."""
    print("🧪 Test de l'API Ultramsg...")
    
    token = os.getenv("ULTRAMSG_TOKEN")
    instance_id = os.getenv("ULTRAMSG_INSTANCE_ID")
    
    if not token or not instance_id:
        print("❌ Token ou Instance ID manquant dans .env")
        return False
    
    # URL de test Ultramsg (endpoint pour obtenir des infos sur l'instance)
    url = f"https://api.ultramsg.com/{instance_id}/instance/status"
    
    params = {"token": token}
    
    try:
        response = requests.get(url, params=params)
        result = response.json()
        
        if response.status_code == 200:
            print("✅ Connexion Ultramsg réussie")
            print(f"📱 Statut de l'instance : {result.get('accountStatus', 'Inconnu')}")
            return True
        else:
            print(f"❌ Erreur API Ultramsg: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_local_server():
    """Tester le serveur local."""
    print("\n🧪 Test du serveur local...")
    
    try:
        # Test du endpoint de santé
        response = requests.get("http://localhost:5005/health", timeout=5)
        
        if response.status_code == 200:
            print("✅ Serveur local accessible")
            print(f"📊 Réponse: {response.json()}")
            return True
        else:
            print(f"❌ Serveur local erreur: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Serveur local non démarré")
        print("💡 Lancez d'abord: python run_ultramsg.py")
        return False
    except Exception as e:
        print(f"❌ Erreur de test serveur: {e}")
        return False

def test_webhook():
    """Simuler un message entrant via webhook."""
    print("\n🧪 Test du webhook...")
    
    webhook_url = "http://localhost:5005/webhooks/ultramsg/webhook"
    
    # Simuler un message Ultramsg
    test_message = {
        "from": "212600000000",  # Numéro de test
        "body": "Bonjour test",
        "type": "text",
        "id": "test_message_123",
        "timestamp": "1234567890"
    }
    
    try:
        response = requests.post(
            webhook_url,
            json=test_message,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Webhook fonctionne")
            print(f"📨 Réponse: {response.json()}")
            return True
        else:
            print(f"❌ Webhook erreur: {response.status_code}")
            print(f"📄 Détails: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de test webhook: {e}")
        return False

def main():
    """Exécuter tous les tests."""
    print("🚀 Tests d'intégration Ultramsg")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: API Ultramsg
    if test_ultramsg_api():
        tests_passed += 1
    
    # Test 2: Serveur local
    if test_local_server():
        tests_passed += 1
    
    # Test 3: Webhook
    if test_webhook():
        tests_passed += 1
    
    # Résultats
    print("\n" + "=" * 50)
    print(f"📊 Résultats: {tests_passed}/{total_tests} tests réussis")
    
    if tests_passed == total_tests:
        print("🎉 Tous les tests sont passés ! Votre bot est prêt.")
        print("💬 Envoyez un message WhatsApp pour tester en réel.")
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez la configuration.")
        
        # Conseils de dépannage
        print("\n💡 Conseils de dépannage:")
        if tests_passed < 1:
            print("- Vérifiez vos credentials Ultramsg dans .env")
        if tests_passed < 2:
            print("- Assurez-vous que le serveur est démarré: python run_ultramsg.py")
        if tests_passed < 3:
            print("- Vérifiez que Rasa est bien configuré et entraîné")

if __name__ == "__main__":
    main()