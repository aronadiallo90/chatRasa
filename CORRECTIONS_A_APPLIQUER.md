# 🔧 Corrections à appliquer après reset

## Problème principal résolu
**Navigation entre menus WhatsApp/Web** - Les choix numériques (1,2,3) interfèrent entre les canaux

## Corrections dans actions.py - ActionHandleMenuSelection

### 1. Amélioration détection contexte (ligne ~1648)
```python
# Récupérer les derniers événements pour comprendre le contexte
events = tracker.events
recent_responses = []
recent_templates = []

for event in reversed(events[-15:]):  # Regarder les 15 derniers événements
    if event.get("event") == "bot":
        # Chercher les templates dans les métadonnées
        metadata = event.get("metadata", {})
        template = metadata.get("template")
        if template:
            recent_templates.append(template)
        
        # Chercher les réponses dans les données
        response = event.get("data", {}).get("response")
        if response:
            recent_responses.append(response)
            
        if len(recent_responses) >= 3 and len(recent_templates) >= 3:
            break

# Combiner les deux listes pour avoir plus de contexte
all_recent_templates = recent_responses + recent_templates
```

### 2. Liste contexte élargie (ligne ~1664)
```python
# Vérifier si on attend une saisie de données (CNI, matricule, etc.)
# OU si on est dans un sous-menu (E-Carrière, PGDE, etc.)
waiting_for_data = any(response in all_recent_templates for response in [
    "utter_ask_cni", "utter_ask_cni_ecarriere", "utter_ask_matricule", 
    "utter_ask_email", "utter_ask_has_account", "utter_ask_has_access",
    "utter_E_carriere", "utter_pgde_menu", "utter_crce_menu", "utter_attestation_menu"
])
```

### 3. Traitement prioritaire des données importantes
```python
# PRIORITÉ 1 : Traiter les données importantes (CNI, matricule) avant tout
# Si le message fait plus de 4 chiffres, c'est probablement des données (CNI, matricule, etc.)
if user_message.isdigit() and len(user_message) > 4:
    print(f"DEBUG ActionHandleMenuSelection: Message trop long ({len(user_message)} chiffres), probablement des données")
    
    # Si c'est un CNI (13 chiffres) et qu'on a une plateforme définie, traiter directement
    platform = tracker.get_slot("platform")
    has_account = tracker.get_slot("has_account")
    
    if len(user_message) == 13 and platform and has_account == "Oui":
        print(f"DEBUG ActionHandleMenuSelection: Traitement direct CNI pour platform={platform}")
        
        if platform == "PGDE":
            return self._handle_pgde_cni(user_message, dispatcher, tracker)
        elif platform == "E-Carrière":
            return self._handle_ecarriere_cni(user_message, dispatcher, tracker)
    
    # Si c'est un matricule pour E-Carrière (après qu'un CNI ait été saisi)
    cni = tracker.get_slot("cni")
    if platform == "E-Carrière" and cni and len(user_message) >= 6:
        print(f"DEBUG ActionHandleMenuSelection: Traitement matricule pour E-Carrière")
        return self._handle_ecarriere_matricule(user_message, cni, dispatcher, tracker)
    
    return []  # Laisser d'autres actions traiter
```

### 4. Traitement canal web amélioré
```python
# Sur web, traiter quand même les données importantes (CNI, matricule) mais pas les choix de menu
if is_web_channel:
    print(f"DEBUG ActionHandleMenuSelection: Canal web détecté (sender_id={tracker.sender_id})")
    
    # Si c'est des données numériques importantes (CNI de 13 chiffres), les traiter quand même
    if user_message.isdigit() and len(user_message) == 13:
        platform = tracker.get_slot("platform")
        has_account = tracker.get_slot("has_account")
        
        if platform and has_account == "Oui":
            print(f"DEBUG ActionHandleMenuSelection: CNI détecté sur canal web pour platform={platform}")
            
            if platform == "PGDE":
                return self._handle_pgde_cni(user_message, dispatcher, tracker)
            elif platform == "E-Carrière":
                return self._handle_ecarriere_cni(user_message, dispatcher, tracker)
    
    # Si c'est un matricule pour E-Carrière (on a déjà un CNI et c'est pas que des chiffres ou plus de 4 caractères)
    platform = tracker.get_slot("platform")
    cni = tracker.get_slot("cni")
    if platform == "E-Carrière" and cni and len(user_message) >= 4:
        print(f"DEBUG ActionHandleMenuSelection: Matricule détecté sur canal web pour E-Carrière")
        return self._handle_ecarriere_matricule(user_message, cni, dispatcher, tracker)
    
    return []  # Laisser d'autres actions traiter les autres cas sur web
```

### 5. Nouvelle méthode _handle_ecarriere_matricule à ajouter
```python
def _handle_ecarriere_matricule(self, matricule: str, cni: str, dispatcher: CollectingDispatcher, tracker: Tracker):
    """Traite les matricules pour E-Carrière après saisie du CNI"""
    try:
        user_data = ECarriereAPIService.verify_user_by_cni_matricule(cni, matricule)
        if user_data:
            projets_list = user_data.get("projets", [])
            message_projets = "\n\n".join(projets_list) if projets_list else "Aucun projet trouvé."
            
            dispatcher.utter_message(
                text=f"🎉 **Compte vérifié avec succès !**\n\nVoici vos 3 derniers projets :\n\n{message_projets}",
                buttons=[
                    {"title": "🔄 Autre vérification", "payload": "/start_account_verification"},
                    {"title": "🏠 Menu principal", "payload": "/go_back_greet_with_name"}
                ]
            )
            return [SlotSet("matricule", matricule), SlotSet("agent_id", user_data.get("agent_id"))]
        else:
            dispatcher.utter_message(response="utter_no_account")
            return []
    except Exception as e:
        print(f"ERREUR _handle_ecarriere_matricule: {e}")
        dispatcher.utter_message(response="utter_server_error")
        return []
```

## Corrections dans data/nlu.yml

### Ajouter "1" et "2" aux intents de choix
```yaml
  - intent: confirm_has_account
    examples: |
      - Oui, j'ai un compte
      - Oui, je suis inscrit
      - J'ai déjà un compte
      - Compte existant
      - Je suis enregistré
      - Oui j'ai un compte
      - Oui
      - 1

  - intent: deny_has_account
    examples: |
      - Non, je n'ai pas de compte
      - Je ne suis pas inscrit
      - Pas de compte
      - Aucun compte
      - Je ne suis pas enregistré
      - Pas de compte existant
      - Non
      - 2

  - intent: confirm_has_access
    examples: |
      - Oui, j'ai accès à mon compte
      - Bien sûr, j'y ai accès
      - Oui, je peux me connecter à mon compte
      - J'ai accès
      - Accès disponible
      - Oui j'ai accès
      - Oui
      - 1

  - intent: deny_has_access
    examples: |
      - Non, je n'ai pas accès
      - Je ne peux pas me connecter
      - Pas d'accès à mon compte
      - Aucun accès
      - Impossible de me connecter
      - Je n'ai pas accès
      - Non
      - 2
```

## Comment appliquer :
1. Revenir au commit fonctionnel : `git reset --hard <commit_hash>`
2. Appliquer ces corrections une par une
3. Tester après chaque modification
4. Entraîner le modèle après les changements NLU : `rasa train`