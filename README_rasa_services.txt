RASA - SERVICES SYSTEMD

Deux services sont installés et démarrent automatiquement :
- rasa-api.service → API HTTP de Rasa
- rasa-actions.service → Serveur d’actions personnalisées

Pour vérifier leur statut :
  sudo systemctl status rasa-api.service
  sudo systemctl status rasa-actions.service

Pour voir les logs :
  sudo journalctl -fu rasa-api.service
  sudo journalctl -fu rasa-actions.service

Pour redémarrer manuellement :
  sudo systemctl restart rasa-api.service
  sudo systemctl restart rasa-actions.service

⚠️ Important :
- Les services utilisent l’environnement virtuel Python dans `.venv`
- Dossier du projet : /home/adminadie/ton_dossier_rasa
