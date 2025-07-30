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


class AccountVerificationForm(FormValidationAction):
    def name(self) -> str:
        return "account_verification_form"
    
    async def extract_has_account(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """Extract has_account value from intent"""
        intent = tracker.latest_message.get("intent", {}).get("name")
        has_account_current = tracker.get_slot("has_account")
        has_access_current = tracker.get_slot("has_access")
        print(f"DEBUG: extract_has_account - intent: {intent}, has_account_current: {has_account_current}, has_access_current: {has_access_current}")
        
        # Si on n'a pas encore has_account, accepter confirm/deny pour has_account
        if has_account_current is None:
            if intent == "confirm_has_account":
                print(f"DEBUG: extract_has_account returning Oui (confirm_has_account)")
                return {"has_account": "Oui"}
            elif intent == "deny_has_account":
                print(f"DEBUG: extract_has_account returning Non (deny_has_account)")
                return {"has_account": "Non"}
            # HACK: Si Rasa confond les intents, accepter aussi confirm_has_access pour has_account
            elif intent == "confirm_has_access":
                print(f"DEBUG: extract_has_account - HACK: treating confirm_has_access as confirm_has_account")
                return {"has_account": "Oui"}
            elif intent == "deny_has_access":
                print(f"DEBUG: extract_has_account - HACK: treating deny_has_access as deny_has_account")
                return {"has_account": "Non"}
        
        print(f"DEBUG: extract_has_account returning None")
        return {"has_account": None}

    async def extract_has_access(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """Extract has_access value from intent"""
        intent = tracker.latest_message.get("intent", {}).get("name")
        requested_slot = tracker.get_slot("requested_slot")
        has_access_current = tracker.get_slot("has_access")
        has_account = tracker.get_slot("has_account")
        print(f"DEBUG: extract_has_access - intent: {intent}, requested_slot: {requested_slot}, has_access_current: {has_access_current}, has_account: {has_account}")
        
        # Si on reçoit confirm/deny_has_access et qu'on a has_account=Oui mais pas encore has_access
        if intent == "confirm_has_access" and has_account == "Oui" and has_access_current is None:
            print(f"DEBUG: extract_has_access returning Oui")
            return {"has_access": "Oui"}
        elif intent == "deny_has_access" and has_account == "Oui" and has_access_current is None:
            print(f"DEBUG: extract_has_access returning Non")
            return {"has_access": "Non"}
        
        print(f"DEBUG: extract_has_access returning None")
        return {"has_access": None}

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Text]:
        """Liste des slots requis à remplir dans le formulaire"""
        print(f"DEBUG: required_slots called. has_account={tracker.get_slot('has_account')}, has_access={tracker.get_slot('has_access')}, email={tracker.get_slot('email')}, cni={tracker.get_slot('cni')}, platform={tracker.get_slot('platform')}")
        
        # Logique séquentielle pour le formulaire
        required = ["has_account"]

        # Si has_account est rempli et = "Oui", demander has_access
        if tracker.get_slot("has_account") == "Oui":
            required.append("has_access")
            
            # Si has_access est rempli et = "Oui", demander email
            if tracker.get_slot("has_access") == "Oui":
                required.append("email")
                
                # Si email est rempli et plateforme = PGDE, demander CNI
                if tracker.get_slot("email") and tracker.get_slot("platform") == "PGDE":
                    required.append("cni")

        print(f"DEBUG: required_slots returning: {required}")
        return required


    async def validate_has_account(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `has_account` value."""
        print(f"DEBUG: validate_has_account called with slot_value: {slot_value}")
        
        # Si la valeur est valide, l'accepter
        if slot_value in ["Oui", "Non"]:
            print(f"DEBUG: validate_has_account returning valid {{'has_account': {slot_value}}}")
            return {"has_account": slot_value}
        
        # Si pas de valeur, poser la question explicitement
        print(f"DEBUG: validate_has_account - no valid value, asking question")
        platform = tracker.get_slot("platform") or "cette plateforme"
        dispatcher.utter_message(response="utter_ask_has_account", platform=platform)
        return {"has_account": None}

    async def validate_has_access(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `has_access` value."""
        print(f"DEBUG: validate_has_access called with slot_value: {slot_value}")
        
        # Si la valeur est valide, l'accepter
        if slot_value in ["Oui", "Non"]:
            print(f"DEBUG: validate_has_access returning valid {{'has_access': {slot_value}}}")
            return {"has_access": slot_value}
        
        # Si pas de valeur, poser la question explicitement
        print(f"DEBUG: validate_has_access - no valid value, asking question")
        dispatcher.utter_message(response="utter_ask_has_access")
        return {"has_access": None}

    async def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `email` value."""
        print(f"DEBUG: validate_email called with slot_value: {slot_value}")
        if tracker.get_slot("has_account") == "Oui" and tracker.get_slot("has_access") == "Oui":
            import re
            email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

            if re.match(email_pattern, slot_value):
                print(f"DEBUG: validate_email returning {{'email': {slot_value}}}")
                return {"email": slot_value}
            dispatcher.utter_message(text="Veuillez entrer une adresse email valide (exemple: nom@domaine.com).")
            print(f"DEBUG: validate_email returning {{'email': None}} after invalid email")
            return {"email": None}
        print(f"DEBUG: validate_email returning {{'email': None}} because has_account or has_access is not Oui")
        return {"email": None}

    async def validate_cni(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate `cni` value."""
        print(f"DEBUG: validate_cni called with slot_value: {slot_value}")
        if tracker.get_slot("platform") == "PGDE" and tracker.get_slot("has_account") == "Oui" and tracker.get_slot("has_access") == "Oui":
            cni_str = str(slot_value).strip()
            if cni_str.isdigit() and len(cni_str) == 13:
                print(f"DEBUG: validate_cni returning {{'cni': {cni_str}}}")
                return {"cni": cni_str}
            dispatcher.utter_message(text="Le numéro de CNI doit contenir exactement 13 chiffres. Veuillez réessayer.")
            print(f"DEBUG: validate_cni returning {{'cni': None}} after invalid cni")
            return {"cni": None}
        print(f"DEBUG: validate_cni returning {{'cni': None}} because platform is not PGDE or has_account/has_access is not Oui")
        return {"cni": None}

    async def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Define what the form has to do
            after all required slots are filled."""

        has_account = tracker.get_slot("has_account")
        has_access = tracker.get_slot("has_access")
        platform = tracker.get_slot("platform")
        email = tracker.get_slot("email")
        cni = tracker.get_slot("cni")

        print(f"DEBUG: submit called. has_account={has_account}, has_access={has_access}, email={email}, cni={cni}, platform={platform}")

        if has_account == "Non":
            dispatcher.utter_message(response="utter_no_account")
        elif has_access == "Non":
            dispatcher.utter_message(response="utter_no_access")
        else:
            # Faire les vérifications email/CNI
            verification_success = self._verify_account_details(email, cni, platform)
            
            if verification_success:
                dispatcher.utter_message(response="utter_account_verified")
                # Conserver les données pour récupération ultérieure du numéro de dossier
                return [SlotSet("has_account", None), SlotSet("has_access", None)]  # Garder email et cni
            else:
                dispatcher.utter_message(
                    text="❌ Désolé, nous ne trouvons pas de compte correspondant à ces informations. Veuillez vérifier votre email et CNI, ou contactez le support technique."
                )
                dispatcher.utter_message(response="utter_no_account")

        print("DEBUG: submit returning SlotSet events")
        return [SlotSet("email", None), SlotSet("cni", None), SlotSet("has_account", None), SlotSet("has_access", None)]

    def _verify_account_details(self, email: str, cni: str, platform: str) -> bool:
        """
        Simuler la vérification des détails du compte.
        En production, ceci ferait appel à une API ou base de données.
        """
        print(f"DEBUG: Vérification compte - email: {email}, cni: {cni}, platform: {platform}")
        
        # Simulation : accepter certains emails/CNI pour les tests
        valid_test_accounts = {
            "test@mpf.sn": "1934200001259",
            "pape.waly@mpf.sn": "9876543210987",
            "demo@fonctionpublique.gouv.sn": "1111111111111"
        }
        
        # Vérifier si c'est un compte de test valide
        if email in valid_test_accounts and cni == valid_test_accounts[email]:
            print(f"DEBUG: Compte valide trouvé pour {email}")
            return True
        
        # Pour la démo, accepter aussi certains patterns
        if platform == "PGDE" and email and cni:
            # Accepter les emails se terminant par @mpf.sn ou @fonctionpublique.gouv.sn
            if (email.endswith("@mpf.sn") or email.endswith("@fonctionpublique.gouv.sn")) and len(cni) == 13:
                print(f"DEBUG: Compte accepté par pattern pour {email}")
                return True
        
        print(f"DEBUG: Aucun compte trouvé pour {email}")
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