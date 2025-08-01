from typing import Any, Text, Dict, List, Optional

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ECarriereAPIService:
    """
    Service pour les appels API E-Carrière avec intégration SQL Server
    """
    
    @staticmethod
    def verify_user_by_cni_matricule(cni: str, matricule: str) -> Optional[Dict[str, Any]]:
        """
        Vérifier si un utilisateur existe par CNI + Matricule dans la base SQL Server
        
        Returns:
            dict: {id: str, nom: str, matricule: str, projets: list} si trouvé
            None: si non trouvé
        """
        try:
            import pyodbc
            
            # Configuration SQL Server
            server = "10.4.116.87,1433"
            database = "referentiel_fudpe_new"
            username = "sa"
            password = "AdieAdie1"
            
            print(f"DEBUG ECarriereAPIService: Tentative de connexion à {server}/{database} avec CNI={cni}, Matricule={matricule}")
            
            # Connexion à SQL Server
            conn = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"UID={username};"
                f"PWD={password}"
            )
            
            cursor = conn.cursor()
            
            # Requête pour récupérer l'utilisateur par CNI + Matricule
            # Utiliser la vraie structure de table agent
            query = """
                SELECT agt_id, agt_cni, agt_matricule_solde, agt_nom, agt_prenom, agt_affectation_id 
                FROM agent 
                WHERE agt_cni = ? AND agt_matricule_solde = ? AND agt_deleted = 0
            """
            
            cursor.execute(query, (cni, matricule))
            user = cursor.fetchone()
            
            print(f"DEBUG ECarriereAPIService: Résultat requête user = {user}")
            
            if user:
                # Requête pour récupérer les 3 derniers projets/actes de l'agent
                actes_query = """
                    SELECT TOP 3
                        ac.act_numero_projet,
                        ac.act_numero_acte,
                        ea.eta_act_code AS etat_projet,
                        ta.tac_libelle AS type_projet
                    FROM 
                        dbo.acte_agent aa
                    INNER JOIN 
                        dbo.acte ac ON ac.act_id = aa.act_agt_act_id
                    LEFT JOIN 
                        dbo.etat_acte ea ON ea.eta_act_id = ac.act_etat_id
                    LEFT JOIN 
                        dbo.type_acte ta ON ta.tac_id = ac.act_tac_id
                    WHERE 
                        aa.act_agt_agt_id = ?
                        AND ac.act_is_projet = 1
                    ORDER BY ac.act_date_acte DESC;
                """
                
                cursor.execute(actes_query, (user[0],)) # user[0] est agt_id
                actes = cursor.fetchall()
                
                # Formater les projets
                projets_list = []
                for acte in actes:
                    projet_info = f"Projet n°{acte[0]} ({acte[3]}) - État: {acte[2]}"
                    projets_list.append(projet_info)
                return {
                    "id": user[0],  # agt_id
                    "nom": f"{user[4]} {user[3]}",  # agt_prenom + agt_nom
                    "matricule": user[2],  # agt_matricule_solde
                    "cni": user[1],  # agt_cni
                    "projets": projets_list
                }
            else:
                print(f"DEBUG ECarriereAPIService: Aucun utilisateur trouvé avec CNI={cni} et Matricule={matricule}")
                return None
            
            return None
            
        except Exception as e:
            print(f"Erreur SQL Server E-Carrière: {e}")
            return None
        
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def verify_user_by_cni(cni: str) -> Optional[Dict[str, Any]]:
        """
        Vérifier si un utilisateur existe par CNI dans la base SQL Server
        
        Returns:
            dict: {id: str, nom: str, matricule: str, projets: list} si trouvé
            None: si non trouvé
        """
        try:
            import pyodbc
            
            # Configuration SQL Server
            server = "10.4.116.87,1433"
            database = "referentiel_fudpe_new"
            username = "sa"
            password = "AdieAdie1"
            
            print(f"DEBUG ECarriereAPIService: Tentative de connexion à {server}/{database} avec CNI={cni}")
            
            # Connexion à SQL Server
            conn = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"UID={username};"
                f"PWD={password}"
            )
            
            cursor = conn.cursor()
            
            # Requête pour récupérer l'utilisateur par CNI
            query = """
                SELECT agt_id, agt_cni, agt_matricule_solde, agt_nom, agt_prenom, agt_affectation_id 
                FROM agent 
                WHERE agt_cni = ? AND agt_deleted = 0
            """
            
            cursor.execute(query, (cni,))
            user = cursor.fetchone()
            
            if user:
                return {
                    "id": user[0],  # agt_id
                    "nom": f"{user[4]} {user[3]}",  # agt_prenom + agt_nom
                    "matricule": user[2],  # agt_matricule_solde
                    "cni": user[1],  # agt_cni
                    "projets": f"Affectation ID: {user[5]}" if user[5] else "Aucune affectation"
                }
            
            return None
            
        except Exception as e:
            print(f"Erreur SQL Server E-Carrière: {e}")
            return None
        
        finally:
            if 'conn' in locals():
                conn.close()


class PGDEAPIService:
    """
    Service pour les appels API PGDE avec intégration MySQL
    """
    
    @staticmethod
    def verify_user_by_cni(cni: str) -> Optional[Dict[str, Any]]:
        """
        Vérifier si un utilisateur existe par CNI dans la base MySQL
        
        Returns:
            dict: {id: str, nom: str, username: str, email: str} si trouvé
            None: si non trouvé
        """
        try:
            import mysql.connector
            from mysql.connector import Error
            
            mysql_config = {
                "host": "127.0.0.1",
                "port": 3306,
                "database": "PGDE",
                "user": "root",
                "password": ""
            }
            
            connection = mysql.connector.connect(**mysql_config)
            cursor = connection.cursor(dictionary=True)
            
            # Requête pour récupérer l'utilisateur par numberid (CNI)
            query = """
                SELECT id, numberid, firstname, lastname, username, email, enabled 
                FROM utilisateur 
                WHERE numberid = %s
            """
            
            cursor.execute(query, (cni,))
            user = cursor.fetchone()
            
            if user:
                return {
                    "id": user['id'],  # Utiliser le numberid comme numéro de dossier
                    "nom": f"{user['firstname']} {user['lastname']}",
                    "username": user['username'],
                    "email": user['email'],
                    "cni": user['numberid']
                }
            
            return None
            
        except Error as e:
            print(f"Erreur MySQL: {e}")
            # Plus de fallback - retourner None si problème BD
            return None
        
        except ImportError:
            print("mysql-connector-python non installé")
            return None
        
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
    
    
    @staticmethod
    def request_password_reset(numberid: str, email: str) -> bool:
        """
        Demander une réinitialisation de mot de passe via API
        
        Returns:
            bool: True si succès, False sinon
        """
        try:
            import requests
            import json
            
            # URL de l'API de réinitialisation
            api_url = "http://127.0.0.1:8000/api/chatbot/reset-password"
            
            # Données à envoyer
            payload = {
                "email": email,
                "numberid": numberid
            }
            
            # Headers
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            # Appel API
            response = requests.post(api_url, data=json.dumps(payload), headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"DEBUG: Reset password API success for {numberid}")
                return True
            else:
                print(f"DEBUG: Reset password API failed - Status: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"DEBUG: API Request failed: {e}")
            # Plus de fallback - retourner False si API ne fonctionne pas
            return False
        
        except ImportError:
            print("DEBUG: requests module not available")
            return False


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
        
        # Extraire le nom via l'entité (Rasa NLU s'occupe de l'extraction)
        nom = next(tracker.get_latest_entity_values("nom"), None)
        
        # Si pas d'entité, essayer le slot nom
        if not nom:
            nom = tracker.get_slot("nom")
        
        # Si toujours pas de nom, prendre le message entier comme nom
        if not nom:
            user_message = tracker.latest_message.get("text", "").strip()
            intent = tracker.latest_message.get("intent", {}).get("name")
            
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
        
        # Nettoyer et formater le nom
        if nom:
            print(f"DEBUG ActionHandleName: nom brut = '{nom}'")
            nom_clean = self._clean_and_format_name(nom)
            print(f"DEBUG ActionHandleName: nom nettoyé = '{nom_clean}'")
            
            if nom_clean and len(nom_clean) > 1:
                dispatcher.utter_message(response="utter_greet_with_name", nom=nom_clean)
                return [SlotSet("nom", nom_clean)]
        
        # Si pas de nom valide, redemander avec aide
        dispatcher.utter_message(text="🤔 **Je n'ai pas bien compris votre nom**\n\n💡 *Vous pouvez dire :*\n• \"Je m'appelle [votre nom]\"\n• \"Mon nom est [votre nom]\"\n• Ou simplement taper votre nom\n\nPouvez-vous réessayer ?")
        return []

    def _clean_and_format_name(self, nom_raw: str) -> str:
        """Nettoie et formate un nom en supprimant les mots parasites"""
        import re
        
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
        
        # Supprimer les mots vides restants
        stop_words = [
            'je', 'suis', 'est', 'me', 'moi', 'mon', 'ma', 'mes', 'le', 'la', 'les', 
            'un', 'une', 'c', 'ce', 'se', 'de', 'du', 'des', 'et', 'nomme', 'appelle',
            'mappel', 'mapel', 'mappelle', 'nom', 'est'
        ]
        
        words = []
        for word in nom_clean.split():
            word_lower = word.lower().strip()
            print(f"DEBUG _clean_and_format_name: mot='{word}', len={len(word)}, in_stop_words={word_lower in stop_words}")
            if word_lower not in stop_words and len(word) > 1:
                words.append(word.title())
        
        result = ' '.join(words).strip()
        print(f"DEBUG _clean_and_format_name: résultat final = '{result}'")
        return result if result else nom_clean.title().strip()


class ActionStartAccountVerification(Action):
    def name(self) -> Text:
        return "action_start_account_verification"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        platform = tracker.get_slot("platform") or "cette plateforme"
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
            SlotSet("user_id", None)
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
                    text="Pas de souci ! 👌\n\nPour créer un compte E-Carrière, vous devez d'abord être un agent de la fonction publique.\n\nVeuillez contacter votre administration pour l'activation de votre compte.",
                    buttons=[
                        {"title": "ℹ️ Comment créer un compte", "payload": "/ask_account_creation"},
                        {"title": "🏢 Retour E-Carrière", "payload": "/go_back_ecarriere"},
                        {"title": "🏠 Menu principal", "payload": "/go_back_greet_with_name"},
                        {"title": "📞 Support", "payload": "/ask_support"}
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
                        text="🎉 Génial ! Vous pouvez vous connecter normalement via ce lien :\n\n🔗 [**Se connecter à E-Carrière**](https://e-carriere.sec.gouv.sn/#/login)\n\n✨ Bonne chance dans vos démarches ! 🤝",
                        buttons=[
                            {"title": "🔄 Autre vérification", "payload": "/start_account_verification"},
                            {"title": "🏠 Menu principal", "payload": "/go_back_greet_with_name"}
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
                dispatcher.utter_message(text="Veuillez entrer une adresse email valide (exemple: nom@domaine.com).")
                return []
        
        return []


    def _verify_and_respond(self, dispatcher, email, cni, platform):
        """Vérification et réponse finale - utilise la vraie BD"""
        if platform == "PGDE" and cni:
            # Utiliser directement l'API PGDE pour vérifier
            user_data = PGDEAPIService.verify_user_by_cni(cni)
            if user_data and user_data.get("email") == email:
                dispatcher.utter_message(response="utter_account_verified")
                return
        
        # Si pas trouvé
        dispatcher.utter_message(
            text="❌ Désolé, nous ne trouvons pas de compte correspondant à ces informations. Veuillez vérifier votre email et CNI, ou contactez le support technique."
        )
        dispatcher.utter_message(response="utter_no_account")


class ActionHandleCNI(Action):
    def name(self) -> Text:
        return "action_handle_cni"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        has_account = tracker.get_slot("has_account")
        platform = tracker.get_slot("platform")
        
        print(f"DEBUG ActionHandleCNI: has_account={has_account}, platform={platform}")
        
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
                    user_data = PGDEAPIService.verify_user_by_cni(cni)
                    
                    if user_data:
                        # Utiliser les vraies données de la base de données
                        nom_officiel = user_data["nom"]
                        username = user_data["username"] 
                        dossier_number = user_data["id"]  # L'ID est le numéro de dossier
                        email = user_data["email"]
                        
                        dispatcher.utter_message(response="utter_account_verified", nom=nom_officiel, username=username, dossier_number=dossier_number)
                        return [SlotSet("cni", cni), SlotSet("nom_officiel", nom_officiel), SlotSet("username", username), SlotSet("dossier_number", dossier_number), SlotSet("email", email), SlotSet("user_id", dossier_number)]
                    else:
                        # Soit CNI n'existe pas, soit problème de connexion BD
                        dispatcher.utter_message(
                            text="❌ **Compte non trouvé**\n\nPossibles causes :\n• CNI inexistant dans la base de données\n• Compte désactivé\n• Problème de connexion à la base de données\n\nVeuillez vérifier votre CNI ou contacter le support."
                        )
                        dispatcher.utter_message(response="utter_no_account")
                        return []
                
                elif platform == "E-Carrière":
                    # E-Carrière : Vérifier d'abord si la CNI existe
                    user_data = ECarriereAPIService.verify_user_by_cni(cni)
                    
                    if user_data:
                        # Si la CNI existe, stocker CNI et demander matricule
                        dispatcher.utter_message(response="utter_ask_matricule")
                        return [SlotSet("cni", cni)]
                    else:
                        # Si la CNI n'existe pas
                        dispatcher.utter_message(
                            text="❌ **Compte non trouvé**\n\nNous n'avons pas trouvé de compte associé à ce numéro de CNI.\n\nVeuillez vérifier votre CNI ou contacter le support.",
                            buttons=[
                                {"title": "🔄 Réessayer", "payload": "/start_account_verification"},
                                {"title": "🏠 Retour E-Carrière", "payload": "/go_back_ecarriere"},
                                {"title": "📞 Support", "payload": "/ask_support"}
                            ]
                        )
                        return []
            else:
                print(f"DEBUG ActionHandleCNI: CNI format invalide - cni={cni}, len={len(cni) if cni else 0}, isdigit={cni.isdigit() if cni else False}")
                dispatcher.utter_message(
                    text="⚠️ **Format incorrect**\n\nLe numéro de CNI doit contenir **12 ou 13 chiffres**.\n\n💡 *Exemples : 178637770865 ou 1934200001259*\n\nVeuillez réessayer :",
                    buttons=[
                        {"title": "🔄 Réessayer", "payload": "/start_account_verification"},
                        {"title": "🏠 Retour E-Carrière", "payload": "/go_back_ecarriere"}
                    ]
                )
                return []
        else:
            print(f"DEBUG ActionHandleCNI: Conditions non remplies - has_account={has_account}, platform={platform}")
        
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
        
        if has_account == "Oui" and platform == "E-Carrière" and cni:
            # Récupérer le matricule du message
            matricule = next(tracker.get_latest_entity_values("matricule"), None)
            if not matricule:
                matricule = tracker.latest_message.get("text", "").strip()
            
            # Valider le matricule (format à adapter selon vos règles)
            if matricule and len(matricule) >= 4:
                # Vérifier avec la base SQL Server
                user_data = ECarriereAPIService.verify_user_by_cni_matricule(cni, matricule)
                
                if user_data:
                    # Utiliser les vraies données de la base SQL Server
                    nom_officiel = user_data["nom"]
                    matricule_official = user_data["matricule"] 
                    agent_id = user_data["id"]
                    projets = user_data["projets"]
                    
                    projets = user_data.get("projets", [])
                    
                    # Formater le message
                    if projets:
                        projets_text = "\n".join([f"- {p}" for p in projets])
                        message = f"""✅ **Compte E-Carrière trouvé !**

Bonjour **{nom_officiel}**,

- **Matricule :** {matricule_official}

Voici vos 3 derniers projets :
{projets_text}"""
                    else:
                        message = f"""✅ **Compte E-Carrière trouvé !**

Bonjour **{nom_officiel}**,

- **Matricule :** {matricule_official}

Nous n'avons pas trouvé de projets récents pour votre compte."""

                    # Envoyer le message avec boutons de navigation
                    dispatcher.utter_message(
                        text=message,
                        buttons=[
                            {"title": "🔄 Autre vérification", "payload": "/start_account_verification"},
                            {"title": "🏢 Retour E-Carrière", "payload": "/go_back_ecarriere"},
                            {"title": "🏠 Menu principal", "payload": "/go_back_greet_with_name"},
                            {"title": "📞 Support", "payload": "/ask_support"}
                        ]
                    )
                    
                    return [SlotSet("matricule", matricule), 
                            SlotSet("nom_officiel", nom_officiel), 
                            SlotSet("agent_id", agent_id)]
                else:
                    dispatcher.utter_message(
                        text="❌ **Compte non trouvé**\n\nPossibles causes :\n• CNI ou Matricule incorrect\n• Compte désactivé\n• Problème de connexion à la base de données\n\nVeuillez vérifier vos informations.",
                        buttons=[
                            {"title": "🔄 Réessayer", "payload": "/start_account_verification"},
                            {"title": "🏠 Retour E-Carrière", "payload": "/go_back_ecarriere"},
                            {"title": "📞 Support", "payload": "/ask_support"}
                        ]
                    )
                    return []
            else:
                dispatcher.utter_message(
                    text="⚠️ **Format incorrect**\n\nVeuillez saisir un matricule valide.\n\n💡 *Exemple : A12345*",
                    buttons=[
                        {"title": "🔄 Réessayer", "payload": "/start_account_verification"},
                        {"title": "🏠 Retour E-Carrière", "payload": "/go_back_ecarriere"}
                    ]
                )
                return []
        else:
            # Debug: Conditions non remplies
            print(f"DEBUG: Conditions non remplies - has_account={has_account}, platform={platform}, cni={cni}")
            dispatcher.utter_message(
                text="⚠️ **Erreur de workflow**\n\nIl semble qu'il y ait un problème avec les informations précédentes. Veuillez recommencer la vérification.",
                buttons=[
                    {"title": "🔄 Recommencer", "payload": "/start_account_verification"},
                    {"title": "🏠 Menu principal", "payload": "/go_back_greet_with_name"}
                ]
            )
            return []
        
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
            success = PGDEAPIService.request_password_reset(cni, email)
            
            if success:
                dispatcher.utter_message(response="utter_password_reset_success", email=email)
            else:
                dispatcher.utter_message(text="❌ **Erreur de réinitialisation**\n\nImpossible d'envoyer l'email de réinitialisation.\n\nPossibles causes :\n• API de réinitialisation indisponible\n• Problème de connexion réseau\n• Email inexistant dans la base\n\nVeuillez contacter le support technique.")
        else:
            dispatcher.utter_message(text="❌ Informations manquantes pour la réinitialisation.")
        
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
            user_data = PGDEAPIService.verify_user_by_cni(cni)
            if user_data:
                dossier_number = user_data["id"]  # ID de la BD
                dispatcher.utter_message(
                    response="utter_dossier_number",
                    dossier_number=dossier_number
                )
                return []
        
        # Si pas de CNI ou utilisateur non trouvé
        dispatcher.utter_message(
            text="❌ Impossible de récupérer le numéro de dossier. Veuillez d'abord vérifier votre compte."
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