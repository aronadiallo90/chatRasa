from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


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

        return [SlotSet("platform", platform)]


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


class ActionStartAccountVerification(Action):
    def name(self) -> Text:
        return "action_start_account_verification"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        platform = tracker.get_slot("platform") or "cette plateforme"
        dispatcher.utter_message(response="utter_ask_has_account", platform=platform)
        return []


class ActionHandleHasAccount(Action):
    def name(self) -> Text:
        return "action_handle_has_account"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        intent = tracker.latest_message.get("intent", {}).get("name")
        
        if intent == "confirm_has_account":
            dispatcher.utter_message(response="utter_ask_has_access")
            return [SlotSet("has_account", "Oui")]
        elif intent == "deny_has_account":
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
        
        if has_account == "Oui":
            if intent == "confirm_has_access":
                dispatcher.utter_message(response="utter_ask_email")
                return [SlotSet("has_access", "Oui")]
            elif intent == "deny_has_access":
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
                dispatcher.utter_message(text="Veuillez entrer une adresse email valide (exemple: nom@domaine.com).")
                return []
        
        return []


    def _verify_and_respond(self, dispatcher, email, cni, platform):
        """Vérification et réponse finale"""
        verification_success = self._verify_account_details(email, cni, platform)
        
        if verification_success:
            dispatcher.utter_message(response="utter_account_verified")
        else:
            dispatcher.utter_message(
                text="❌ Désolé, nous ne trouvons pas de compte correspondant à ces informations. Veuillez vérifier votre email et CNI, ou contactez le support technique."
            )
            dispatcher.utter_message(response="utter_no_account")

    def _verify_account_details(self, email: str, cni: str, platform: str) -> bool:
        """Vérification des détails du compte"""
        valid_test_accounts = {
            "test@mpf.sn": "1934200001259",
            "pape.waly@mpf.sn": "9876543210987",
            "demo@fonctionpublique.gouv.sn": "1111111111111"
        }
        
        if email in valid_test_accounts and (cni == valid_test_accounts[email] or cni is None):
            return True
        
        if platform == "PGDE" and email and cni:
            if (email.endswith("@mpf.sn") or email.endswith("@fonctionpublique.gouv.sn")) and len(cni) == 13:
                return True
        
        return False


class ActionHandleCNI(Action):
    def name(self) -> Text:
        return "action_handle_cni"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        has_account = tracker.get_slot("has_account")
        has_access = tracker.get_slot("has_access")
        email = tracker.get_slot("email")
        platform = tracker.get_slot("platform")
        
        if has_account == "Oui" and has_access == "Oui" and email:
            # Récupérer le CNI du message
            cni = next(tracker.get_latest_entity_values("cni"), None)
            if not cni:
                cni = tracker.latest_message.get("text", "").strip()
            
            # Valider le CNI
            if cni and cni.isdigit() and len(cni) == 13:
                # Vérifier le compte
                self._verify_and_respond(dispatcher, email, cni, platform)
                return [SlotSet("cni", cni)]
            else:
                dispatcher.utter_message(text="Le numéro de CNI doit contenir exactement 13 chiffres. Veuillez réessayer.")
                return []
        
        return []

    def _verify_and_respond(self, dispatcher, email, cni, platform):
        """Vérification et réponse finale"""
        verification_success = self._verify_account_details(email, cni, platform)
        
        if verification_success:
            dispatcher.utter_message(response="utter_account_verified")
        else:
            dispatcher.utter_message(
                text="❌ Désolé, nous ne trouvons pas de compte correspondant à ces informations. Veuillez vérifier votre email et CNI, ou contactez le support technique."
            )
            dispatcher.utter_message(response="utter_no_account")

    def _verify_account_details(self, email: str, cni: str, platform: str) -> bool:
        """Vérification des détails du compte"""
        valid_test_accounts = {
            "test@mpf.sn": "1934200001259",
            "pape.waly@mpf.sn": "9876543210987",
            "demo@fonctionpublique.gouv.sn": "1111111111111"
        }
        
        if email in valid_test_accounts and cni == valid_test_accounts[email]:
            return True
        
        if platform == "PGDE" and email and cni:
            if (email.endswith("@mpf.sn") or email.endswith("@fonctionpublique.gouv.sn")) and len(cni) == 13:
                return True
        
        return False


class ActionGetDossierNumber(Action):
    def name(self) -> Text:
        return "action_get_dossier_number"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Simuler la récupération du numéro de dossier
        # En production, ceci ferait appel à une API ou base de données
        email = tracker.get_slot("email")
        cni = tracker.get_slot("cni")
        
        # Simulation d'un numéro de dossier basé sur l'email/CNI
        if email and cni:
            # Générer un numéro de dossier simulé
            dossier_number = f"PGDE-{cni[-4:]}-{hash(email) % 10000:04d}"
        else:
            # Numéro par défaut si pas d'infos
            dossier_number = "PGDE-0000-0001"
        
        dispatcher.utter_message(
            response="utter_dossier_number",
            dossier_number=dossier_number
        )
        
        return []