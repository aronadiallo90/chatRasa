from typing import Any, Text, Dict, List, Optional

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import ActionExecuted, SessionStarted, SlotSet
import sys
import json
from datetime import datetime
import hashlib
import os
import re

# Accès aux données : PGDE via l'API emplois, E-Carrière via SQL Server ou API (backend_api.py).
from .backend_api import (
    CODE_INACTIVE_ACCOUNT,
    CODE_NOT_FOUND,
    CODE_RESET_ACCEPTED,
    CODE_TOO_MANY_REQUESTS,
    BackendAPIError,
    PGDEBackendService,
    build_ecarriere_service,
)


# E-Carrière : SQL Server direct ou API selon CHATBOT_ECARRIERE_MODE (legacy par défaut).
ECarriereAPIService = build_ecarriere_service()
PGDEAPIService = PGDEBackendService()


PLATFORM_BUTTONS = [
    {"title": "E-Carrière", "payload": "/choose_platform{\"platform\": \"E-Carrière\"}"},
    {"title": "Demande d'emploi (PGDE)", "payload": "/choose_platform{\"platform\": \"PGDE\"}"},
    {"title": "Attestation de non appartenance", "payload": "/choose_platform{\"platform\": \"Attestation\"}"}
]

# Seules ces informations survivent à une longue inactivité (voir session_config du domain).
# CNI, email, compte vérifié… sont volontairement effacés : poste partagé possible (cybercafé).
SLOTS_KEPT_BETWEEN_SESSIONS = ("platform", "nom")
# Un prénom/nom plausible : lettres (accents compris), espaces, tirets, apostrophes ; 4 mots max.
VALID_NAME_PATTERN = re.compile(r"^[^\W\d_][^\W\d_' -]*(?:[ '-][^\W\d_]+){0,3}$")
NAME_REFUSAL_PATTERN = re.compile(
    r"^(non|nan|no|pas de nom)\b|\b(ne|n')\s*(veux|souhaite|préfère|prefere)\b|\bpréfère pas\b|\brefuse\b",
    re.IGNORECASE,
)


def is_name_refusal(message: str) -> bool:
    """« non », « je ne veux pas »… — mais pas « Pascal » ni « Nana »."""
    return bool(NAME_REFUSAL_PATTERN.search(message.strip()))


def valid_name_or_none(candidate: str) -> Optional[str]:
    """Nom mis en forme s'il ressemble à un nom (2 à 40 caractères), sinon None."""
    cleaned = " ".join(candidate.split())
    if not 2 <= len(cleaned) <= 40 or not VALID_NAME_PATTERN.match(cleaned):
        return None
    return cleaned


def utter_not_understood(dispatcher: CollectingDispatcher, platform: Optional[str], nom: Optional[str]) -> None:
    """Message incompris : on le dit et on propose des choix utiles, au lieu de rester muet."""
    buttons: List[Dict[Text, Any]] = []
    if platform == "E-Carrière":
        buttons.append({"title": "Retour E-Carrière", "payload": "/go_back_ecarriere"})
    elif platform == "PGDE":
        buttons.append({"title": "Retour PGDE", "payload": "/go_back_pgde"})
    if nom:
        buttons.append({"title": "Menu principal", "payload": "/go_back_greet_with_name"})
    else:
        buttons.extend(PLATFORM_BUTTONS)
    buttons.append({"title": "Support", "payload": "/ask_support"})
    dispatcher.utter_message(
        text="Je n'ai pas bien compris votre demande.\nVeuillez choisir une option ci-dessous :",
        buttons=buttons,
    )
# Nom officiel affiché par Amath : modifiable sans réentraîner le modèle.
MINISTERE_NOM_PAR_DEFAUT = "Ministère de la Fonction publique, du Travail et de la Réforme du Service public"


class ActionSessionStart(Action):
    """Nouvelle session après inactivité : on garde la plateforme et le prénom, rien d'autre."""

    def name(self) -> Text:
        return "action_session_start"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ministere = os.getenv("CHATBOT_MINISTERE_NOM", "").strip() or MINISTERE_NOM_PAR_DEFAUT
        events: List[Dict[Text, Any]] = [SessionStarted(), SlotSet("ministere", ministere)]
        for slot_name in SLOTS_KEPT_BETWEEN_SESSIONS:
            slot_value = tracker.get_slot(slot_name)
            if slot_value is not None:
                events.append(SlotSet(slot_name, slot_value))
        events.append(ActionExecuted("action_listen"))
        return events


def _utter_backend_unavailable(dispatcher: CollectingDispatcher, error: BackendAPIError,
                               retry_payload: str = "/start_account_verification") -> None:
    """Message unique pour toute panne backend (indisponible, refus, réponse hors contrat)."""
    print(f"ERREUR backend: {error} (code={error.code}, correlation_id={error.correlation_id})")
    dispatcher.utter_message(
        text="**Problème temporaire**\n\nNous rencontrons des difficultés techniques. Veuillez réessayer dans quelques instants.",
        buttons=[
            {"title": "Réessayer", "payload": retry_payload},
            {"title": "Menu principal", "payload": "/go_back_greet_with_name"},
            {"title": "Support", "payload": "/ask_support"}
        ]
    )


def _utter_pgde_inactive_account(dispatcher: CollectingDispatcher, user_data: Dict[str, Any]) -> None:
    """Compte PGDE trouvé mais non activé (email jamais confirmé) ou suspendu."""
    nom_officiel = user_data.get("nom") or "Utilisateur"
    dispatcher.utter_message(
        text=f"**Compte non activé**\n\nBonjour **{nom_officiel}**, votre compte PGDE existe mais il n'est pas actif.\n\nCliquez sur le lien d'activation reçu par email lors de votre inscription.\n\nSi vous ne l'avez pas reçu ou si votre compte a été suspendu, contactez le support.",
        buttons=[
            {"title": "Autre vérification", "payload": "/start_account_verification"},
            {"title": "Menu principal", "payload": "/go_back_greet_with_name"},
            {"title": "Support", "payload": "/ask_support"}
        ]
    )


class ActionRedirectPlatform(Action):
    def name(self) -> Text:
        return "action_redirect_platform"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        platform = tracker.get_slot("platform")
        if not platform:
            platform_entity = next(tracker.get_latest_entity_values("platform"), None)
            if platform_entity:
                platform = platform_entity

        # Reset des données d'autres plateformes lors du changement
        reset_slots = [
            SlotSet("email", None),
            SlotSet("cni", None),
            SlotSet("username", None),
            SlotSet("dossier_number", None),
            SlotSet("nom_officiel", None),
            SlotSet("user_id", None),
            SlotSet("has_account", None),
            SlotSet("has_access", None)
        ]

        if platform == "E-Carrière":
            dispatcher.utter_message(response="utter_E_carriere")
        elif platform == "PGDE":
            dispatcher.utter_message(response="utter_pgde_menu")
        elif platform == "CRCE":
            dispatcher.utter_message(response="utter_crce_menu")
        elif platform == "Attestation":
            dispatcher.utter_message(response="utter_attestation_menu")
        else:
            dispatcher.utter_message(text="Je ne suis pas sûr de la plateforme que vous avez choisie. Pouvez-vous réessayer ?")
            dispatcher.utter_message(response="utter_greet_with_name")
            return [SlotSet("platform", None)]

        return [SlotSet("platform", platform)] + reset_slots


class ActionExplainAccountCreation(Action):
    def name(self) -> Text:
        return "action_explain_account_creation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        platform = tracker.get_slot("platform")

        if platform == "E-Carrière":
            dispatcher.utter_message(response="utter_ask_account_creation")
        elif platform == "PGDE":
            dispatcher.utter_message(response="utter_ask_pgde_account_creation")
        elif platform == "CRCE":
            dispatcher.utter_message(response="utter_crce_menu")
        elif platform == "Attestation":
            dispatcher.utter_message(response="utter_attestation_menu")
        else:
            dispatcher.utter_message(response="utter_ask_account_creation")

        return []


class ActionExplainLogin(Action):
    def name(self) -> Text:
        return "action_explain_login"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        platform = tracker.get_slot("platform")

        if platform == "E-Carrière":
            dispatcher.utter_message(response="utter_ask_login")
        elif platform == "PGDE":
            dispatcher.utter_message(response="utter_ask_pgde_login")
        else:
            dispatcher.utter_message(response="utter_ask_login")

        return []


class ActionExplainPasswordReset(Action):
    def name(self) -> Text:
        return "action_explain_password_reset"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        platform = tracker.get_slot("platform")

        if platform == "E-Carrière":
            dispatcher.utter_message(response="utter_ask_password_reset")
        elif platform == "PGDE":
            dispatcher.utter_message(response="utter_ask_pgde_password_reset")
        else:
            dispatcher.utter_message(response="utter_ask_password_reset")

        return []


class ActionHandleName(Action):
    def name(self) -> Text:
        return "action_handle_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_message = tracker.latest_message.get("text", "").strip()
        intent_name = tracker.latest_message.get("intent", {}).get("name", "")

        # Refus explicite (« non », « je ne veux pas »…) : on continue sans nom
        if intent_name == "refuse_name" or is_name_refusal(user_message):
            dispatcher.utter_message(
                text="Pas de problème !\n\nJe peux vous aider même sans connaître votre nom.\n\n**Quelle plateforme vous intéresse ?**",
                buttons=PLATFORM_BUTTONS,
            )
            return [SlotSet("nom", "Utilisateur")]

        # Le nom vient du message EN COURS (entité, sinon texte saisi) : jamais de l'ancien slot,
        # sinon « Arona » saisi après « Baba » affichait encore « Bienvenue, Baba ».
        nom = next(tracker.get_latest_entity_values("nom"), None)
        if not nom:
            intent = intent_name
            
            # Ignorer certains intents spécifiques
            ignore_intents = [
                "greet", "choose_platform", "ask_account_creation", "ask_login", 
                "ask_password_reset", "go_back_greet_with_name", "go_back_ecarriere",
                "go_back_pgde", "go_back_autres", "ask_support", "fallback",
                "confirm_has_account", "deny_has_account", "confirm_has_access",
                "deny_has_access", "provide_email", "provide_cni"
            ]
            
            if intent not in ignore_intents and user_message:
                nom = user_message
        
        # Nettoyer, mettre en forme et vérifier que ça ressemble à un nom
        # Le texte brut est vérifié AVANT nettoyage : « dfokn,gb » ne doit pas devenir « Dfokngb »
        saisie_plausible = bool(nom) and not re.search(r"[^\w\s'’.-]|[\d_]", nom)
        nom_valide = valid_name_or_none(self._clean_and_format_name(nom)) if saisie_plausible else None
        if nom_valide:
            dispatcher.utter_message(response="utter_greet_with_name", nom=nom_valide)
            return [SlotSet("nom", nom_valide)]

        # Chiffres, symboles, une seule lettre… : on redemande en expliquant
        dispatcher.utter_message(
            text="Je n'ai pas reconnu de nom dans votre message.\n\n"
                 "**Pourriez-vous m'indiquer votre nom ?** (lettres uniquement)\n"
                 "Sinon, tapez « non » pour continuer sans nom."
        )
        return []

    def _clean_and_format_name(self, nom_raw: str) -> str:
        """Nettoie et formate un nom en supprimant les mots parasites"""
        import re
        
        # NOUVEAU: Vérifier d'abord les mots de refus/négation
        refusal_words = [
            'non', 'pas', 'ne', 'jamais', 'rien', 'aucun', 'aucune', 'personne',
            'refuse', 'veux', 'want', 'peut', 'peux', 'pourquoi', 'comment',
            'quand', 'où', 'quoi', 'qui', 'combien', 'lequel', 'laquelle'
        ]
        
        nom_lower = nom_raw.lower().strip()
        
        # Si le message entier est un mot de refus, retourner vide
        if nom_lower in refusal_words:
            print(f"DEBUG _clean_and_format_name: Mot de refus détecté: '{nom_raw}'")
            return ""
        
        # Si le message contient uniquement des mots de refus, retourner vide
        words_in_message = nom_lower.split()
        if all(word in refusal_words for word in words_in_message):
            print(f"DEBUG _clean_and_format_name: Message composé uniquement de mots de refus: '{nom_raw}'")
            return ""
        
        # Patterns pour extraire seulement le nom (après les expressions courantes)
        extraction_patterns = [
            r"je\s+m['\']?ap+el+\w*\s+(.+)",     # je m'appelle X → X
            r"je\s+ma?p+el+\w*\s+(.+)",          # je mapel X → X  
            r"je\s+me\s+nomme\s+(.+)",           # je me nomme X → X
            r"mo?n\s+no?m\s+[eéc]+st?\s+(.+)",   # mon nom est X → X
            r"mo?n\s+no?m\s+(.+)",               # mon nom X → X
            r"c['']?est\s+(.+)",                 # c'est X → X
            r"se\s+(.+)",                        # se X → X (faute)
            r"moi\s+c['']?est\s+(.+)",           # moi c'est X → X
            r"je\s+suis\s+(.+)",                 # je suis X → X
        ]
        
        nom_extracted = nom_raw.strip()
        
        # Essayer d'extraire avec les patterns
        for pattern in extraction_patterns:
            match = re.search(pattern, nom_raw.lower())
            if match:
                nom_extracted = match.group(1).strip()
                break
        
        # Nettoyer les caractères spéciaux
        nom_clean = re.sub(r'[^\w\s\-\'àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ]', '', nom_extracted)
        
        # Supprimer les mots vides restants + mots de refus
        stop_words = [
            'je', 'suis', 'est', 'me', 'moi', 'mon', 'ma', 'mes', 'le', 'la', 'les', 
            'un', 'une', 'c', 'ce', 'se', 'de', 'du', 'des', 'et', 'nomme', 'appelle',
            'mappel', 'mapel', 'mappelle', 'nom', 'est'
        ] + refusal_words  # Ajouter les mots de refus aux stop_words
        
        words = []
        for word in nom_clean.split():
            word_lower = word.lower().strip()
            print(f"DEBUG _clean_and_format_name: mot='{word}', len={len(word)}, in_stop_words={word_lower in stop_words}")
            if word_lower not in stop_words and len(word) > 1:
                words.append(word.title())
        
        result = ' '.join(words).strip()
        
        # NOUVEAU: Validation supplémentaire - un nom doit faire au moins 2 caractères
        if len(result) < 2:
            print(f"DEBUG _clean_and_format_name: Nom trop court après nettoyage: '{result}'")
            return ""
        
        print(f"DEBUG _clean_and_format_name: résultat final = '{result}'")
        return result


class ActionStartAccountVerification(Action):
    def name(self) -> Text:
        return "action_start_account_verification"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        platform = tracker.get_slot("platform")
        if not platform:
            # Plateforme perdue (ex. longue inactivité) : la redemander plutôt que de
            # partir dans un parcours générique qui ne sait vérifier aucun compte.
            dispatcher.utter_message(
                text="**Reprenons**\n\nPour quelle plateforme souhaitez-vous vérifier votre compte ?",
                buttons=PLATFORM_BUTTONS
            )
            return []

        dispatcher.utter_message(response="utter_ask_has_account", platform=platform)

        # Reset des données de vérification précédente
        return [
            SlotSet("has_account", None),
            SlotSet("has_access", None),
            SlotSet("email", None),
            SlotSet("cni", None),
            SlotSet("username", None),
            SlotSet("dossier_number", None),
            SlotSet("nom_officiel", None),
            SlotSet("user_id", None),
            SlotSet("matricule", None),
            SlotSet("agent_id", None)
        ]


class ActionHandleHasAccount(Action):
    def name(self) -> Text:
        return "action_handle_has_account"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        intent = tracker.latest_message.get("intent", {}).get("name")
        platform = tracker.get_slot("platform")
        
        if intent == "confirm_has_account":
            if platform == "PGDE":
                # Pour PGDE : demander CNI directement
                dispatcher.utter_message(response="utter_ask_cni")
            elif platform == "E-Carrière":
                # Pour E-Carrière : demander CNI d'abord
                dispatcher.utter_message(response="utter_ask_cni_ecarriere")
            else:
                # Pour autres plateformes : demander accès
                dispatcher.utter_message(response="utter_ask_has_access")
            return [SlotSet("has_account", "Oui")]
        elif intent == "deny_has_account":
            # Adapter le message selon la plateforme
            if platform == "E-Carrière":
                dispatcher.utter_message(
                    text="Prêt à suivre votre carrière en quelques clics ?\nPour créer votre compte sur **E-Carrière** et accéder à vos services, vous devez disposer d'un **matricule de solde**.",
                    buttons=[
                        {"title": "Activer mon compte", "payload": "/ask_account_creation"},
                        {"title": "Retour E-Carrière", "payload": "/go_back_ecarriere"},
                        {"title": "Menu principal", "payload": "/go_back_greet_with_name"},
                        {"title": "Support", "payload": "/ask_support"}
                    ]
                )
            elif platform == "PGDE":
                dispatcher.utter_message(
                    text="Pas de souci !\n\nLa **PGDE** est ouverte à tous les Sénégalais. Vous pouvez créer votre compte facilement :",
                    buttons=[
                        {"title": "Créer mon compte", "payload": "/ask_account_creation"},
                        {"title": "Retour PGDE", "payload": "/go_back_pgde"},
                        {"title": "Menu principal", "payload": "/go_back_greet_with_name"},
                        {"title": "Support", "payload": "/ask_support"}
                    ]
                )
            else:
                dispatcher.utter_message(response="utter_no_account")
            return [SlotSet("has_account", "Non")]
        
        return []


class ActionHandleHasAccess(Action):
    def name(self) -> Text:
        return "action_handle_has_access"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        intent = tracker.latest_message.get("intent", {}).get("name")
        has_account = tracker.get_slot("has_account")
        platform = tracker.get_slot("platform")
        
        if has_account == "Oui":
            if intent == "confirm_has_access":
                if platform == "PGDE":
                    # Pour PGDE : confirmer connexion
                    dispatcher.utter_message(response="utter_account_access_confirmed")
                elif platform == "E-Carrière":
                    # Pour E-Carrière : confirmer connexion
                    dispatcher.utter_message(
                        text="Génial ! Vous pouvez vous connecter normalement via ce lien :\n\n[**Se connecter à E-Carrière**](https://e-carriere.sec.gouv.sn/#/login)\n\nBonne chance dans vos démarches !",
                        buttons=[
                            {"title": "Autre vérification", "payload": "/start_account_verification"},
                            {"title": "Menu principal", "payload": "/go_back_greet_with_name"}
                        ]
                    )
                else:
                    # Pour autres plateformes : demander email
                    dispatcher.utter_message(response="utter_ask_email")
                return [SlotSet("has_access", "Oui")]
            elif intent == "deny_has_access":
                if platform == "PGDE":
                    # Pour PGDE : demander confirmation avant réinitialisation
                    # Utiliser le nom officiel si disponible, sinon le nom saisi
                    nom_display = tracker.get_slot("nom_officiel") or tracker.get_slot("nom") or "Utilisateur"
                    email = tracker.get_slot("email") or "votre email"
                    dispatcher.utter_message(response="utter_confirm_password_reset", nom=nom_display, email=email)
                else:
                    # Pour autres plateformes : options générales
                    dispatcher.utter_message(response="utter_no_access")
                return [SlotSet("has_access", "Non")]
        
        return []


class ActionHandleEmail(Action):
    def name(self) -> Text:
        return "action_handle_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        has_account = tracker.get_slot("has_account")
        has_access = tracker.get_slot("has_access")
        platform = tracker.get_slot("platform")
        
        if has_account == "Oui" and has_access == "Oui":
            # Récupérer l'email du message
            email = next(tracker.get_latest_entity_values("email"), None)
            if not email:
                email = tracker.latest_message.get("text", "").strip()
            
            # Valider l'email
            import re
            email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            
            if email and re.match(email_pattern, email):
                if platform == "PGDE":
                    dispatcher.utter_message(response="utter_ask_cni")
                else:
                    # Vérifier directement sans CNI pour autres plateformes
                    self._verify_and_respond(dispatcher, email, None, platform)
                return [SlotSet("email", email)]
            else:
                dispatcher.utter_message(text="**Adresse email non valide**\n Assurez-vous d'entrer une adresse email au bon format, comme exemple@gmail.com.")
                return []
        
        return []


    def _verify_and_respond(self, dispatcher, email, cni, platform):
        """Vérification et réponse finale - utilise la vraie BD"""
        if platform == "PGDE" and cni:
            # Utiliser directement l'API PGDE pour vérifier
            try:
                user_data = PGDEAPIService.verify_user_by_cni(cni)
            except BackendAPIError as error:
                _utter_backend_unavailable(dispatcher, error)
                return
            if user_data and (user_data.get("email") or "").lower() == email.lower():
                if not user_data["actif"]:
                    _utter_pgde_inactive_account(dispatcher, user_data)
                    return
                dispatcher.utter_message(response="utter_account_verified")
                return
        
        # Si pas trouvé (un seul message : utter_no_account contient déjà le texte et les boutons)
        dispatcher.utter_message(response="utter_no_account")


class ActionHandleCNI(Action):
    def name(self) -> Text:
        return "action_handle_cni"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        has_account = tracker.get_slot("has_account")
        platform = tracker.get_slot("platform")
        existing_cni = tracker.get_slot("cni")
        
        print(f"DEBUG ActionHandleCNI: has_account='{has_account}', platform='{platform}', existing_cni='{existing_cni}'")
        
        # Fix immédiat pour PGDE - traiter directement si CNI de 13 chiffres
        latest_text = tracker.latest_message.get("text", "").strip()
        if platform == "PGDE" and latest_text.isdigit() and len(latest_text) == 13:
            print(f"DEBUG ActionHandleCNI: Traitement direct PGDE pour CNI '{latest_text}'")
            try:
                user_data = PGDEAPIService.verify_user_by_cni(latest_text)
                if user_data and not user_data["actif"]:
                    _utter_pgde_inactive_account(dispatcher, user_data)
                    return []
                if user_data:
                    nom_officiel = user_data["nom"]
                    username = user_data["username"]
                    dossier_number = user_data["id"]
                    email = user_data["email"]

                    dispatcher.utter_message(response="utter_account_verified", nom=nom_officiel, username=username, dossier_number=dossier_number)
                    return [SlotSet("cni", latest_text), SlotSet("nom_officiel", nom_officiel), SlotSet("username", username), SlotSet("dossier_number", dossier_number), SlotSet("email", email), SlotSet("user_id", dossier_number), SlotSet("has_account", "Oui")]
                else:
                    dispatcher.utter_message(response="utter_no_account")
                    return []
            except BackendAPIError as error:
                _utter_backend_unavailable(dispatcher, error)
                return []
            except Exception as e:
                print(f"ERREUR ActionHandleCNI PGDE: {e}")
                dispatcher.utter_message(response="utter_server_error")
                return []
        
        # Si on a déjà un CNI et qu'on est sur E-Carrière, vérifier si c'est le même CNI ou un nouveau
        latest_text = tracker.latest_message.get("text", "").strip()
        if existing_cni and platform == "E-Carrière":
            # Si c'est le même CNI, ignorer 
            if existing_cni == latest_text:
                print(f"DEBUG ActionHandleCNI: Même CNI '{latest_text}' déjà présent, ignorer")
                return []
            # Si c'est un CNI différent, on le traite
            elif latest_text.isdigit() and len(latest_text) == 13:
                print(f"DEBUG ActionHandleCNI: Nouveau CNI '{latest_text}' détecté, traiter")
                # Continue le traitement normal
            else:
                print("DEBUG ActionHandleCNI: CNI déjà présent, on attend probablement un matricule")
                return []
        
        if has_account == "Oui" and (platform == "PGDE" or platform == "E-Carrière"):
            # Récupérer le CNI du message
            cni = next(tracker.get_latest_entity_values("cni"), None)
            if not cni:
                cni = tracker.latest_message.get("text", "").strip()
            
            print(f"DEBUG ActionHandleCNI: CNI extracted = {cni}")
            
            # Valider le CNI - accepter 12 ou 13 chiffres
            if cni and cni.isdigit() and len(cni) >= 12 and len(cni) <= 13:
                if platform == "PGDE":
                    # PGDE : Vérification directe avec CNI
                    try:
                        user_data = PGDEAPIService.verify_user_by_cni(cni)
                    except BackendAPIError as error:
                        _utter_backend_unavailable(dispatcher, error)
                        return []

                    if user_data and not user_data["actif"]:
                        _utter_pgde_inactive_account(dispatcher, user_data)
                        return []
                    if user_data:
                        # Utiliser les vraies données de la base de données
                        nom_officiel = user_data["nom"]
                        username = user_data["username"] 
                        dossier_number = user_data["id"]  # L'ID est le numéro de dossier
                        email = user_data["email"]
                        
                        dispatcher.utter_message(response="utter_account_verified", nom=nom_officiel, username=username, dossier_number=dossier_number)
                        return [SlotSet("cni", cni), SlotSet("nom_officiel", nom_officiel), SlotSet("username", username), SlotSet("dossier_number", dossier_number), SlotSet("email", email), SlotSet("user_id", dossier_number)]
                    else:
                        # CNI inconnue : un seul message, avec les mêmes boutons que utter_no_account
                        dispatcher.utter_message(
                            text="**Nous n'avons pas pu retrouver votre compte.**\n\nLe numéro de CNI saisi ne correspond à aucun compte dans nos systèmes.\n\nVeuillez vérifier l'exactitude de votre CNI ou contacter notre équipe d'assistance si besoin.",
                            buttons=[
                                {"title": "Créer mon compte", "payload": "/ask_account_creation"},
                                {"title": "Réessayer", "payload": "/start_account_verification"},
                                {"title": "Menu principal", "payload": "/go_back_greet_with_name"},
                                {"title": "Support", "payload": "/ask_support"}
                            ]
                        )
                        return []
                
                elif platform == "E-Carrière":
                    # E-Carrière : Vérifier d'abord si la CNI existe
                    try:
                        user_data = ECarriereAPIService.verify_user_by_cni(cni)
                        
                        if user_data:
                            # Si la CNI existe, stocker CNI et demander matricule
                            dispatcher.utter_message(response="utter_ask_matricule")
                            return [SlotSet("cni", cni)]
                        else:
                            # Si la CNI n'existe pas
                            dispatcher.utter_message(
                                text="**Compte non trouvé**\n\nNous n'avons pas trouvé de compte avec ce numéro de CNI.\n\nVérifiez votre numéro ou contactez le support si besoin.",
                                buttons=[
                                    {"title": "Réessayer", "payload": "/start_account_verification"},
                                    {"title": "Retour E-Carrière", "payload": "/go_back_ecarriere"},
                                    {"title": "Support", "payload": "/ask_support"}
                                ]
                            )
                            return []
                    except Exception as e:
                        print(f"ERREUR dans ActionHandleCNI: {e}")
                        dispatcher.utter_message(
                            text="**Problème temporaire**\n\nNous rencontrons des difficultés techniques. Veuillez réessayer dans quelques instants.",
                            buttons=[
                                {"title": "Réessayer", "payload": "/start_account_verification"},
                                {"title": "Retour E-Carrière", "payload": "/go_back_ecarriere"}
                            ]
                        )
                        return []
            else:
                print(f"DEBUG ActionHandleCNI: CNI format invalide - cni={cni}, len={len(cni) if cni else 0}, isdigit={cni.isdigit() if cni else False}")
                dispatcher.utter_message(
                    text="**Format de CNI incorrect**\n\nVotre numéro de CNI doit contenir exactement 13 chiffres.\n\nVérifiez sur votre carte d'identité et ressaisissez.",
                    buttons=[
                        {"title": "Réessayer", "payload": "/start_account_verification"},
                        {"title": "Retour E-Carrière", "payload": "/go_back_ecarriere"}
                    ]
                )
                return []
        else:
            print(f"DEBUG ActionHandleCNI: Conditions non remplies - has_account={has_account}, platform={platform}")
            # Si on arrive ici, quelque chose ne va pas dans le flux
            # Saisie hors parcours de vérification (ex. « 1 » au menu) : ce n'est pas une erreur
            utter_not_understood(dispatcher, platform, tracker.get_slot("nom"))
        
        return []



class ActionHandleMatricule(Action):
    def name(self) -> Text:
        return "action_handle_matricule"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        has_account = tracker.get_slot("has_account")
        platform = tracker.get_slot("platform")
        cni = tracker.get_slot("cni")
        
        print(f"DEBUG ActionHandleMatricule: has_account={has_account}, platform={platform}, cni={cni}")
        
        latest_intent = tracker.latest_message.get("intent", {}).get("name")
        latest_text = tracker.latest_message.get("text", "")
        print(f"DEBUG ActionHandleMatricule: latest_intent={latest_intent}, latest_text='{latest_text}'")
        
        # Fix pour PGDE : Si c'est PGDE et que le texte est un CNI (13 chiffres), traiter comme CNI
        if platform == "PGDE" and latest_text.isdigit() and len(latest_text) == 13:
            print(f"DEBUG ActionHandleMatricule: PGDE détecté avec CNI '{latest_text}', rediriger vers traitement CNI")
            try:
                user_data = PGDEAPIService.verify_user_by_cni(latest_text)
                if user_data and not user_data["actif"]:
                    _utter_pgde_inactive_account(dispatcher, user_data)
                    return []
                if user_data:
                    nom_officiel = user_data["nom"]
                    username = user_data["username"]
                    dossier_number = user_data["id"]
                    email = user_data["email"]

                    dispatcher.utter_message(response="utter_account_verified", nom=nom_officiel, username=username, dossier_number=dossier_number)
                    return [SlotSet("cni", latest_text), SlotSet("nom_officiel", nom_officiel), SlotSet("username", username), SlotSet("dossier_number", dossier_number), SlotSet("email", email), SlotSet("user_id", dossier_number)]
                else:
                    dispatcher.utter_message(response="utter_no_account")
                    return []
            except BackendAPIError as error:
                _utter_backend_unavailable(dispatcher, error)
                return []
            except Exception as e:
                print(f"ERREUR ActionHandleMatricule PGDE: {e}")
                dispatcher.utter_message(response="utter_server_error")
                return []
        
        # Vérifier si l'input ressemble à un CNI (13 chiffres)
        input_text = latest_text.strip()
        is_input_cni = input_text.isdigit() and len(input_text) == 13
        
        # Fix: Si on a déjà un CNI dans le slot ET qu'on reçoit le même CNI, on n'a rien à faire
        # (éviter le retraitement du même CNI)
        if platform == "E-Carrière" and cni and is_input_cni and cni == input_text:
            print(f"DEBUG ActionHandleMatricule: Même CNI '{input_text}' déjà traité, ignorer")
            return []
        
        # Si on n'a pas de CNI OU si l'input est un nouveau CNI différent
        if platform == "E-Carrière" and (not cni or (is_input_cni and cni != input_text)):
            
            # Détecter si c'est un CNI (13 chiffres uniquement)
            if is_input_cni:
                print("DEBUG ActionHandleMatricule: Input est un CNI, rediriger vers traitement CNI")
                # Traiter directement comme un CNI
                try:
                    user_data = ECarriereAPIService.verify_user_by_cni(input_text)
                    if user_data:
                        dispatcher.utter_message(response="utter_ask_matricule")
                        return [SlotSet("cni", input_text)]
                    else:
                        dispatcher.utter_message(
                            text="**Compte non trouvé**\n\nNous n'avons pas trouvé de compte avec ce numéro de CNI.\n\nVérifiez votre numéro ou contactez le support si besoin.",
                            buttons=[
                                {"title": "Réessayer", "payload": "/start_account_verification"},
                                {"title": "Retour E-Carrière", "payload": "/go_back_ecarriere"},
                                {"title": "Support", "payload": "/ask_support"}
                            ]
                        )
                        return []
                except Exception as e:
                    print(f"ERREUR dans ActionHandleMatricule (CNI processing): {e}")
                    dispatcher.utter_message(
                        text="**Problème temporaire**\n\nNous rencontrons des difficultés techniques. Veuillez réessayer dans quelques instants.",
                        buttons=[
                            {"title": "Réessayer", "payload": "/start_account_verification"},
                            {"title": "Retour E-Carrière", "payload": "/go_back_ecarriere"}
                        ]
                    )
                    return []
            
            # Si ce n'est pas un CNI, peut-être un matricule mal classifié  
            elif not cni and self._is_valid_matricule_format(input_text):
                print("DEBUG ActionHandleMatricule: Input ressemble à un matricule, mais CNI manquant")
                dispatcher.utter_message(
                    text="**CNI requis d'abord**\n\nPour vérifier votre matricule, j'ai d'abord besoin de votre numéro de CNI (13 chiffres).\n\nVeuillez saisir votre CNI :",
                    buttons=[
                        {"title": "Recommencer", "payload": "/start_account_verification"},
                        {"title": "Retour E-Carrière", "payload": "/go_back_ecarriere"}
                    ]
                )
                return []
        
        if has_account == "Oui" and platform == "E-Carrière" and cni:
            # Récupérer le matricule du message
            matricule = next(tracker.get_latest_entity_values("matricule"), None)
            if not matricule:
                matricule = tracker.latest_message.get("text", "").strip()
            
            # Vérifier si l'utilisateur saisit un CNI au lieu d'un matricule
            if matricule and matricule.isdigit() and len(matricule) == 13:
                print(f"DEBUG ActionHandleMatricule: Utilisateur saisit CNI '{matricule}' au lieu de matricule")
                dispatcher.utter_message(
                    text="**Vous avez saisi un CNI au lieu d'un matricule**\n\nNous attendons votre **matricule** (6-9 chiffres + 1 lettre).\n\nExemples : `123456A`, `654986B`\n\nVotre CNI est déjà enregistré. Veuillez maintenant saisir votre matricule :",
                    buttons=[
                        {"title": "Réessayer", "payload": "/start_account_verification"},
                        {"title": "Retour E-Carrière", "payload": "/go_back_ecarriere"}
                    ]
                )
                return []
            
            # Nettoyer et valider le matricule
            matricule_clean = self._clean_matricule(matricule) if matricule else None
            print(f"DEBUG ActionHandleMatricule: matricule brut='{matricule}', matricule nettoyé='{matricule_clean}'")
            
            if matricule_clean and self._is_valid_matricule_format(matricule_clean):
                # Vérifier via l'API E-Carrière en utilisant le matricule nettoyé
                try:
                    user_data = ECarriereAPIService.verify_user_by_cni_matricule(cni, matricule_clean)
                except BackendAPIError as error:
                    _utter_backend_unavailable(dispatcher, error, "/go_back_ecarriere")
                    return []

                if user_data:
                    nom_officiel = user_data["nom"]
                    matricule_official = user_data["matricule"]
                    agent_id = user_data["id"]
                    agent_email = user_data.get("email")
                    projets = user_data.get("projets", [])

                    # L'activation est désormais fournie par le backend (champ actif / code INACTIVE_ACCOUNT)
                    compte_active = user_data["actif"]
                    
                    # Message de salutation
                    message = f"""Enchanté **{nom_officiel}**,

- **Matricule :** {matricule_official}
"""
                    
                    # Ajouter message d'activation si nécessaire
                    if not compte_active:
                        message += """\n**Activation requise**
Je vois que vous n'avez pas encore activé votre compte E-Carrière.
Veillez le faire pour accéder à la plateforme E-Carrière en ligne.

"""

                    # Boutons de choix selon les données disponibles
                    buttons = []
                    if projets:
                        message += "Que souhaitez-vous faire ?"
                        buttons.extend([
                            {"title": "Voir mes actes", "payload": "/voir_actes"},
                            {"title": "Voir mes projets", "payload": "/voir_projets"}
                        ])
                    else:
                        message += "Aucun projet ou acte n'est disponible pour votre compte pour le moment."
                    
                    # Ajouter bouton d'activation si nécessaire
                    if not compte_active:
                        buttons.append({"title": "Activer mon compte", "payload": "/ask_account_creation"})
                    
                    # Ajouter option de réinitialisation mot de passe si compte activé ET email disponible
                    if compte_active and agent_email:
                        buttons.append({"title": "Réinitialiser mot de passe", "payload": "/reset_password_ecarriere"})
                    
                    # Boutons de navigation
                    buttons.extend([
                        {"title": "Autre vérification", "payload": "/start_account_verification"},
                        {"title": "Retour E-Carrière", "payload": "/go_back_ecarriere"},
                        {"title": "Menu principal", "payload": "/go_back_greet_with_name"},
                        {"title": "Support", "payload": "/ask_support"}
                    ])

                    # Envoyer le message avec boutons de choix
                    dispatcher.utter_message(text=message, buttons=buttons)
                    
                    return [SlotSet("matricule", matricule_clean), 
                            SlotSet("nom_officiel", nom_officiel), 
                            SlotSet("agent_id", agent_id),
                            SlotSet("email", agent_email)]
                else:
                    dispatcher.utter_message(
                        text="**Nous n'avons pas pu retrouver votre compte.**\n\nLe matricule saisi ne correspond pas à votre CNI dans nos systèmes.\n\nVeuillez vérifier l'exactitude de votre matricule ou contacter notre équipe d'assistance si besoin.",
                        buttons=[
                            {"title": "Réessayer", "payload": "/start_account_verification"},
                            {"title": "Retour E-Carrière", "payload": "/go_back_ecarriere"},
                            {"title": "Support", "payload": "/ask_support"}
                        ]
                    )
                    return []
            else:
                dispatcher.utter_message(
                    text="**Format de matricule incorrect**\n\nLe matricule doit contenir :\n• 6 à 9 chiffres + 1 lettre\n• Exemple : `123456A` ou `123456789B`\n\n*Les slash \"/\" sont automatiquement supprimés*",
                    buttons=[
                        {"title": "Réessayer", "payload": "/start_account_verification"},
                        {"title": "Retour E-Carrière", "payload": "/go_back_ecarriere"}
                    ]
                )
                return []
        else:
            # Debug: Conditions non remplies
            print(f"DEBUG: Conditions non remplies - has_account={has_account}, platform={platform}, cni={cni}")
            # Saisie hors parcours de vérification (ex. « 1 » au menu) : ce n'est pas une erreur
            utter_not_understood(dispatcher, platform, tracker.get_slot("nom"))
            return []
        
        return []
    
    def _clean_matricule(self, matricule_raw: str) -> str:
        """Nettoie le matricule selon les règles définies."""
        import re
        
        if not matricule_raw:
            return ""
            
        # Supprimer les espaces
        matricule = matricule_raw.strip()
        
        # Supprimer les slashes "/"
        matricule = re.sub(r'/', '', matricule)
        
        # Mettre la lettre finale en majuscule
        # Pattern: 6-9 chiffres suivis d'une lettre
        match = re.match(r'^(\d{6,9})([a-zA-Z])$', matricule)
        if match:
            chiffres, lettre = match.groups()
            matricule = chiffres + lettre.upper()
        
        print(f"DEBUG _clean_matricule: '{matricule_raw}' -> '{matricule}'")
        return matricule
    
    def _is_valid_matricule_format(self, matricule: str) -> bool:
        """Valide le format du matricule: 6-9 chiffres + 1 lettre majuscule."""
        import re
        
        if not matricule:
            return False
            
        # Pattern: exactement 6-9 chiffres suivis d'exactement 1 lettre majuscule
        pattern = r'^[0-9]{6,9}[A-Z]$'
        is_valid = bool(re.match(pattern, matricule))
        
        print(f"DEBUG _is_valid_matricule_format: '{matricule}' -> {is_valid}")
        return is_valid


class ActionResetPasswordECarriere(Action):
    """Demander confirmation pour réinitialisation mot de passe E-Carrière"""
    def name(self) -> Text:
        return "action_reset_password_ecarriere"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        nom_officiel = tracker.get_slot("nom_officiel") or "Utilisateur"
        email = tracker.get_slot("email")
        
        if email:
            dispatcher.utter_message(
                text=f"**Réinitialisation mot de passe E-Carrière**\n\nBonjour **{nom_officiel}**,\n\nVoulez-vous réinitialiser votre mot de passe E-Carrière ?\n\nUn email sera envoyé à : **{email}**\n\nCette action ne peut pas être annulée.",
                buttons=[
                    {"title": "Confirmer réinitialisation", "payload": "/confirm_reset_ecarriere"},
                    {"title": "Annuler", "payload": "/cancel_reset_ecarriere"},
                    {"title": "Retour au menu", "payload": "/retour_menu_utilisateur"}
                ]
            )
        else:
            dispatcher.utter_message(
                text="**Email non trouvé**\n\nNous n'avons pas trouvé d'adresse email associée à votre compte.\n\nVeuillez contacter le support technique.",
                buttons=[
                    {"title": "Retour au menu", "payload": "/retour_menu_utilisateur"},
                    {"title": "Support", "payload": "/ask_support"}
                ]
            )
        
        return []


class ActionConfirmResetECarriere(Action):
    """Confirmer et effectuer la réinitialisation E-Carrière"""
    def name(self) -> Text:
        return "action_confirm_reset_ecarriere"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        email = tracker.get_slot("email")
        nom_officiel = tracker.get_slot("nom_officiel") or "Utilisateur"
        
        if email:
            # Appel API de réinitialisation
            try:
                reset_code = ECarriereAPIService.request_password_reset_ecarriere(email)
            except BackendAPIError as error:
                _utter_backend_unavailable(dispatcher, error, "/reset_password_ecarriere")
                return []

            if reset_code == CODE_RESET_ACCEPTED:
                dispatcher.utter_message(
                    text=f"**Votre demande de réinitialisation a été envoyée avec succès.**\n\nConsultez votre boîte email : **{email}**\n\nSuivez les instructions dans l'email pour créer un nouveau mot de passe.",
                    buttons=[
                        {"title": "Retour au menu", "payload": "/retour_menu_utilisateur"},
                        {"title": "Menu principal", "payload": "/go_back_greet_with_name"}
                    ]
                )
            else:
                dispatcher.utter_message(
                    text=f"**Échec de la réinitialisation**\n\nDésolé **{nom_officiel}**,\n\nNous n'avons pas pu traiter votre demande de réinitialisation.\nVeuillez réessayer plus tard ou contacter le support technique pour assistance.",
                    buttons=[
                        {"title": "Réessayer", "payload": "/reset_password_ecarriere"},
                        {"title": "Retour au menu", "payload": "/retour_menu_utilisateur"},
                        {"title": "Support", "payload": "/ask_support"}
                    ]
                )
        else:
            dispatcher.utter_message(
                text="**Informations manquantes**\n\nNous ne trouvons pas votre email. Veuillez recommencer la vérification.",
                buttons=[
                    {"title": "Recommencer", "payload": "/start_account_verification"},
                    {"title": "Menu principal", "payload": "/go_back_greet_with_name"}
                ]
            )
        
        return []


class ActionHandleFallbackAfterGreet(Action):
    """Gérer le fallback après demande de nom - traiter comme refus de nom"""
    def name(self) -> Text:
        return "action_handle_fallback_after_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Après « pourriez-vous me communiquer votre nom », le texte saisi EST la réponse :
        # même traitement que action_handle_name (refus, nom valide, ou nouvelle demande).
        return ActionHandleName().run(dispatcher, tracker, domain)

    def _ancien_traitement(self, dispatcher: CollectingDispatcher, tracker: Tracker) -> List[Dict[Text, Any]]:
        events = tracker.events
        last_user_message = None
        
        # Chercher le dernier UserUttered avant le possible UserUtteranceReverted
        for event in reversed(events):
            if event.get("event") == "user":
                last_user_message = event.get("text", "").lower().strip()
                break
        
        print(f"DEBUG ActionHandleFallbackAfterGreet: dernier message = '{last_user_message}'")
        
        # Si c'est un message de refus, traiter comme refus de nom
        refusal_patterns = ['non', 'pas', 'ne veux pas', 'refuse', 'ne souhaite pas', 'préfère pas']
        
        if last_user_message and any(pattern in last_user_message for pattern in refusal_patterns):
            print(f"DEBUG ActionHandleFallbackAfterGreet: Refus détecté, redirection vers menu")
            dispatcher.utter_message(
                text="Pas de problème !\n\nJe peux vous aider même sans connaître votre nom.\n\n**Quelle plateforme vous intéresse ?**",
                buttons=[
                    {"title": "E-Carrière", "payload": "/choose_platform{\"platform\": \"E-Carrière\"}"},
                    {"title": "Demande d'emploi (PGDE)", "payload": "/choose_platform{\"platform\": \"PGDE\"}"},
                    {"title": "Attestation de non appartenance", "payload": "/choose_platform{\"platform\": \"Attestation\"}"}
                ]
            )
            return [SlotSet("nom", "Utilisateur")]
        else:
            # Sinon, demander le nom à nouveau
            dispatcher.utter_message(text="**Pour mieux vous aider, j'aimerais connaître votre nom.**\n\nSinon, tapez 'non' pour continuer sans nom.")
            return []


class ActionFallbackMenu(Action):
    """Message incompris en cours de conversation : réponse explicite au lieu d'un silence."""

    def name(self) -> Text:
        return "action_fallback_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        utter_not_understood(dispatcher, tracker.get_slot("platform"), tracker.get_slot("nom"))
        return []


class ActionCancelResetECarriere(Action):
    """Annuler la réinitialisation E-Carrière"""
    def name(self) -> Text:
        return "action_cancel_reset_ecarriere"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        nom_officiel = tracker.get_slot("nom_officiel") or "Utilisateur"
        
        dispatcher.utter_message(
            text=f"**Réinitialisation annulée**\n\nPas de problème **{nom_officiel}** !\n\nLa réinitialisation de votre mot de passe a été annulée.\n\nVotre mot de passe actuel reste inchangé.",
            buttons=[
                {"title": "Retour au menu", "payload": "/retour_menu_utilisateur"},
                {"title": "Menu principal", "payload": "/go_back_greet_with_name"}
            ]
        )
        
        return []


class ActionConfirmPasswordReset(Action):
    def name(self) -> Text:
        return "action_confirm_password_reset"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        cni = tracker.get_slot("cni")
        email = tracker.get_slot("email")
        
        if cni and email:
            # Appel API réel avec numberid (CNI)
            try:
                reset_code = PGDEAPIService.request_password_reset(cni, email)
            except BackendAPIError as error:
                _utter_backend_unavailable(dispatcher, error, "/confirm_password_reset")
                return []

            if reset_code == CODE_RESET_ACCEPTED:
                dispatcher.utter_message(response="utter_password_reset_success", email=email)
            elif reset_code == CODE_INACTIVE_ACCOUNT:
                _utter_pgde_inactive_account(dispatcher, {"nom": tracker.get_slot("nom_officiel")})
            elif reset_code == CODE_TOO_MANY_REQUESTS:
                dispatcher.utter_message(
                    text="**Demande déjà en cours**\n\nUn email de réinitialisation vient déjà d'être envoyé. Consultez votre boîte de réception (et les spams) ou réessayez dans quelques minutes.",
                    buttons=[
                        {"title": "Menu principal", "payload": "/go_back_greet_with_name"},
                        {"title": "Support", "payload": "/ask_support"}
                    ]
                )
            elif reset_code == CODE_NOT_FOUND:
                dispatcher.utter_message(
                    text="**Informations incohérentes**\n\nL'email et la CNI ne correspondent pas au même compte. Veuillez recommencer la vérification.",
                    buttons=[
                        {"title": "Autre vérification", "payload": "/start_account_verification"},
                        {"title": "Support", "payload": "/ask_support"}
                    ]
                )
            else:
                dispatcher.utter_message(
                    text="**Réinitialisation non aboutie**\n\nUne erreur est survenue lors de l'envoi de l'email de réinitialisation.\n\nVous pouvez réessayer dans un instant ou contacter le support technique pour obtenir de l'aide.",
                    buttons=[
                        {"title": "Réessayer", "payload": "/confirm_password_reset"},
                        {"title": "Autre vérification", "payload": "/start_account_verification"},
                        {"title": "Menu principal", "payload": "/go_back_greet_with_name"},
                        {"title": "Support", "payload": "/ask_support"}
                    ]
                )
        else:
            dispatcher.utter_message(
                text="**Informations manquantes**\n\nDonnées nécessaires pour la réinitialisation introuvables.\n\nVeuillez recommencer le processus.",
                buttons=[
                    {"title": "Recommencer", "payload": "/start_account_verification"},
                    {"title": "Menu principal", "payload": "/go_back_greet_with_name"},
                    {"title": "Support", "payload": "/ask_support"}
                ]
            )
        
        return []


class ActionDenyPasswordReset(Action):
    def name(self) -> Text:
        return "action_deny_password_reset"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(response="utter_password_reset_cancelled")
        return []


class ActionGetDossierNumber(Action):
    def name(self) -> Text:
        return "action_get_dossier_number"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Récupérer le numéro de dossier depuis la BD via CNI
        cni = tracker.get_slot("cni")
        
        if cni:
            try:
                user_data = PGDEAPIService.verify_user_by_cni(cni)
            except BackendAPIError as error:
                _utter_backend_unavailable(dispatcher, error)
                return []
            if user_data:
                dossier_number = user_data["id"]  # ID de la BD
                dispatcher.utter_message(
                    response="utter_dossier_number",
                    dossier_number=dossier_number
                )
                return []
        
        # Si pas de CNI ou utilisateur non trouvé
        dispatcher.utter_message(
            text="Impossible de récupérer le numéro de dossier. Veuillez d'abord vérifier votre compte."
        )
        return []


class ActionResetAccountData(Action):
    """Reset les données de compte pour une nouvelle vérification"""
    def name(self) -> Text:
        return "action_reset_account_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return [
            SlotSet("email", None),
            SlotSet("cni", None),
            SlotSet("username", None),
            SlotSet("dossier_number", None),
            SlotSet("nom_officiel", None),
            SlotSet("user_id", None),
            SlotSet("has_account", None),
            SlotSet("has_access", None)
        ]


class ActionResetForNewPlatform(Action):
    """Reset données spécifiques quand on change de plateforme"""
    def name(self) -> Text:
        return "action_reset_for_new_platform"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Garder nom et nouvelle plateforme, reset le reste
        return [
            SlotSet("email", None),
            SlotSet("cni", None),
            SlotSet("username", None),
            SlotSet("dossier_number", None),
            SlotSet("nom_officiel", None),
            SlotSet("user_id", None),
            SlotSet("has_account", None),
            SlotSet("has_access", None)
        ]


class ActionSoftReset(Action):
    """Reset léger - garde les infos de base mais reset le processus"""
    def name(self) -> Text:
        return "action_soft_reset"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Garde nom, platform, mais reset les données temporaires
        return [
            SlotSet("has_account", None),
            SlotSet("has_access", None)
        ]


class ActionVoirActes(Action):
    """Affiche tous les actes de l'utilisateur"""
    def name(self) -> Text:
        return "action_voir_actes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        cni = tracker.get_slot("cni")
        matricule = tracker.get_slot("matricule")
        nom_officiel = tracker.get_slot("nom_officiel")
        
        if cni and matricule:
            # Récupérer tous les actes de l'utilisateur
            agent_id = tracker.get_slot("agent_id")
            try:
                user_data = ECarriereAPIService.get_all_actes(agent_id) if agent_id else None
            except BackendAPIError as error:
                _utter_backend_unavailable(dispatcher, error, "/voir_actes")
                return []
            
            if user_data and user_data.get("actes"):
                actes = user_data["actes"]
                actes_text = "\n\n".join(actes)
                
                message = f"""**Vos 3 derniers actes, {nom_officiel}**

{actes_text}"""
            else:
                message = f"""**Aucun acte disponible pour le moment, {nom_officiel}**

Votre espace ne contient pas d'actes actuellement. Si vous pensez que c'est une erreur, vous pouvez contacter le support."""
        else:
            message = "Informations incomplètes.\nIl semble que certaines informations soient manquantes.\nVeuillez recommencer le processus depuis le début."

        dispatcher.utter_message(
            text=message,
            buttons=[
                {"title": "Retour au menu", "payload": "/retour_menu_utilisateur"},
                {"title": "Menu principal", "payload": "/go_back_greet_with_name"}
            ]
        )
        
        return []


class ActionVoirProjets(Action):
    """Affiche les projets de l'utilisateur"""
    def name(self) -> Text:
        return "action_voir_projets"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        cni = tracker.get_slot("cni")
        matricule = tracker.get_slot("matricule")
        nom_officiel = tracker.get_slot("nom_officiel")
        
        if cni and matricule:
            # Récupérer les projets de l'utilisateur
            agent_id = tracker.get_slot("agent_id")
            try:
                user_data = ECarriereAPIService.get_projets(agent_id) if agent_id else None
            except BackendAPIError as error:
                _utter_backend_unavailable(dispatcher, error, "/voir_projets")
                return []
            
            if user_data and user_data.get("projets"):
                projets = user_data["projets"]
                projets_text = "\n\n".join(projets)
                
                titre_projets = "Votre dernier projet" if len(projets) == 1 else f"Vos {len(projets)} derniers projets"
                message = f"""**{titre_projets}, {nom_officiel}**

{projets_text}"""
            else:
                message = f"""**Aucun projet trouvé, {nom_officiel}**

Aucun projet n'apparaît pour votre compte pour le moment.
N'hésitez pas à contacter le support si besoin."""
        else:
            message = "Erreur : Informations d'authentification manquantes."
        
        dispatcher.utter_message(
            text=message,
            buttons=[
                {"title": "Retour au menu", "payload": "/retour_menu_utilisateur"},
                {"title": "Menu principal", "payload": "/go_back_greet_with_name"}
            ]
        )
        
        return []


class ActionAucunProjetActe(Action):
    """Gère le cas où il n'y a pas de projets ou d'actes"""
    def name(self) -> Text:
        return "action_aucun_projet_acte"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        nom_officiel = tracker.get_slot("nom_officiel") or "Utilisateur"
        
        dispatcher.utter_message(
            text=f"**Aucun projet ou acte disponible, {nom_officiel}**\n\nNous n'avons trouvé aucun projet ou acte associé à votre compte pour le moment.\n\nVeuillez contacter le support si vous pensez qu'il s'agit d'une erreur.",
            buttons=[
                {"title": "Nouvelle vérification", "payload": "/start_account_verification"},
                {"title": "Menu principal", "payload": "/go_back_greet_with_name"},
                {"title": "Support", "payload": "/ask_support"}
            ]
        )
        
        return []


class ActionRetourMenuUtilisateur(Action):
    """Retourne au menu de choix utilisateur après authentification"""
    def name(self) -> Text:
        return "action_retour_menu_utilisateur"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        nom_officiel = tracker.get_slot("nom_officiel")
        matricule_official = tracker.get_slot("matricule")
        cni = tracker.get_slot("cni")
        matricule = tracker.get_slot("matricule")
        
        if nom_officiel and matricule_official:
            # Vérifier la disponibilité des projets/actes et récupérer email + statut activation
            try:
                user_data = ECarriereAPIService.verify_user_by_cni_matricule(cni, matricule)
            except BackendAPIError as error:
                _utter_backend_unavailable(dispatcher, error, "/retour_menu_utilisateur")
                return []
            projets = user_data.get("projets", []) if user_data else []
            agent_email = user_data.get("email") if user_data else None
            compte_active = user_data["actif"] if user_data else False
            
            message = f"""Enchanté **{nom_officiel}**,

- **Matricule :** {matricule_official}

Que souhaitez-vous consulter ?"""

            # Boutons de choix selon les données disponibles
            buttons = []
            if projets:
                buttons.extend([
                    {"title": "Voir mes actes", "payload": "/voir_actes"},
                    {"title": "Voir mes projets", "payload": "/voir_projets"}
                ])
            else:
                buttons.append({"title": "Aucun projet/acte disponible", "payload": "/aucun_projet_acte"})
            
            # Ajouter option de réinitialisation mot de passe si compte activé ET email disponible
            if compte_active and agent_email:
                buttons.append({"title": "Réinitialiser mot de passe", "payload": "/reset_password_ecarriere"})
            
            # Boutons de navigation
            buttons.extend([
                {"title": "Autre vérification", "payload": "/start_account_verification"},
                {"title": "Menu principal", "payload": "/go_back_greet_with_name"}
            ])

            dispatcher.utter_message(text=message, buttons=buttons)
        else:
            dispatcher.utter_message(
                text="Erreur : Informations d'authentification manquantes. Veuillez recommencer la vérification.",
                buttons=[
                    {"title": "Recommencer", "payload": "/start_account_verification"},
                    {"title": "Menu principal", "payload": "/go_back_greet_with_name"}
                ]
            )
        
        return []
