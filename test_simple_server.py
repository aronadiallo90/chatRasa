#!/usr/bin/env python3
"""
🧪 Serveur Flask simple pour tester le webhook
"""

from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/webhooks/ultramsg/webhook", methods=["POST"])
def webhook():
    """Test simple du webhook"""
    try:
        data = request.get_json()
        print(f"📨 Données reçues: {json.dumps(data, indent=2)}")
        
        if data.get("event_type") == "message_received":
            message_body = data["data"]["body"]
            sender_id = data["data"]["from"]
            print(f"✅ Message: '{message_body}' de {sender_id}")
            return jsonify({"status": "success", "message": "Message reçu"})
        
        return jsonify({"status": "ignored", "message": "Event type non traité"})
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return {"status": "Serveur test actif", "endpoint": "/webhooks/ultramsg/webhook"}

if __name__ == "__main__":
    print("🧪 Démarrage serveur test sur port 5007...")
    app.run(host="0.0.0.0", port=5007, debug=True)