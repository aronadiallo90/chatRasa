#!/usr/bin/env python3
"""
🧪 Test du tunnel localtunnel
"""

import requests

def test_tunnel():
    """Tester la connexion au tunnel"""
    url = "https://silver-queens-cut.loca.lt/health"
    headers = {"bypass-tunnel-reminder": "true"}
    
    try:
        print("🧪 Test du tunnel...")
        response = requests.get(url, headers=headers)
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Réponse: {response.text}")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    test_tunnel()