#!/usr/bin/env python3
"""
🌐 Alternative à ngrok pour exposer le serveur local
Utilise localhost.run (gratuit, sans inscription)
"""

import subprocess
import threading
import time
import sys
import os

def start_tunnel(port=8080):
    """Démarrer un tunnel SSH avec localhost.run"""
    print(f"🌐 Création du tunnel pour le port {port}...")
    print("💡 Alternative gratuite à ngrok")
    
    try:
        # Commande SSH pour localhost.run
        cmd = f"ssh -R 80:localhost:{port} nokey@localhost.run"
        
        print(f"📝 Commande à exécuter dans un autre terminal :")
        print(f"   {cmd}")
        print()
        print("🔗 Ou copiez cette commande dans PowerShell/CMD :")
        print(f"   ssh -R 80:localhost:{port} nokey@localhost.run")
        print()
        print("⚠️  Si SSH n'est pas installé, utilisez plutôt :")
        print("   1. Téléchargez ngrok: https://ngrok.com/download")
        print(f"   2. Ou utilisez: npx localtunnel --port {port}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

def install_localtunnel():
    """Instructions pour installer localtunnel"""
    print("📦 Installation de localtunnel (alternative Node.js) :")
    print("   npm install -g localtunnel")
    print(f"   npx localtunnel --port {os.getenv('PORT', 8080)}")

if __name__ == "__main__":
    port = int(os.getenv('PORT', 8080))
    
    print("🚀 Options pour exposer votre serveur local :")
    print("=" * 50)
    
    print("\n🔹 Option 1: localhost.run (SSH)")
    start_tunnel(port)
    
    print("\n🔹 Option 2: localtunnel (Node.js)")
    install_localtunnel()
    
    print("\n🔹 Option 3: ngrok (recommandé)")
    print("   1. Télécharger: https://ngrok.com/download")
    print("   2. Extraire ngrok.exe dans ce dossier")
    print(f"   3. Exécuter: ./ngrok http {port}")
    
    print("\n💡 Une fois le tunnel créé, copiez l'URL HTTPS")
    print("   et configurez-la dans votre dashboard Ultramsg")