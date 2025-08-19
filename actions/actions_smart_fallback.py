from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionHandleUnexpectedInput(Action):
    """Gère les saisies inattendues quand des boutons sont attendus"""
    def name(self) -> Text:
        return "action_handle_unexpected_input"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Récupérer le contexte actuel
        platform = tracker.get_slot("platform")
        nom = tracker.get_slot("nom") or "Utilisateur"
        
        # Analyser la dernière intention pour comprendre le contexte
        latest_intent = tracker.latest_message.get("intent", {}).get("name")
        user_text = tracker.latest_message.get("text", "").strip()
        
        # Messages contextuels selon la situation
        if platform:
            context_message = f"Nous discutons de **{platform}**."
        else:
            context_message = "Nous choisissons une plateforme."
        
        # Réponse adaptée selon l'input
        if latest_intent == "greet":
            dispatcher.utter_message(
                text=f"Salut {nom} ! 👋\n\n{context_message} Utilisez les boutons pour continuer notre conversation.",
                buttons=[
                    {"title": "🔄 Retour au menu", "payload": "/go_back_greet_with_name"},
                    {"title": "📞 Support", "payload": "/ask_support"}
                ]
            )
        elif latest_intent == "fallback" or not latest_intent:
            dispatcher.utter_message(
                text=f"🤔 Je n'ai pas bien compris \"{user_text}\".\n\n{context_message} Utilisez les boutons disponibles pour une meilleure navigation.",
                buttons=[
                    {"title": "🔄 Retour au menu", "payload": "/go_back_greet_with_name"},
                    {"title": "📞 Support", "payload": "/ask_support"}
                ]
            )
        else:
            # Rediriger selon l'intent détecté
            if latest_intent == "ask_support":
                dispatcher.utter_message(response="utter_ask_support")
            elif latest_intent == "choose_platform":
                # Extraire la plateforme si possible
                platform_entity = next(tracker.get_latest_entity_values("platform"), None)
                if platform_entity:
                    return [SlotSet("platform", platform_entity)]
                else:
                    dispatcher.utter_message(
                        text=f"Je vois que vous voulez choisir une plateforme ! Voici les options :",
                        buttons=[
                            {"title": "🏢 E-Carrière", "payload": "/choose_platform{\"platform\": \"E-Carrière\"}"},
                            {"title": "📋 PGDE", "payload": "/choose_platform{\"platform\": \"PGDE\"}"},
                            {"title": "🏛️ CRCE", "payload": "/choose_platform{\"platform\": \"CRCE\"}"},
                            {"title": "📄 Attestation", "payload": "/choose_platform{\"platform\": \"Attestation\"}"}
                        ]
                    )
            else:
                dispatcher.utter_message(
                    text=f"✨ D'accord {nom} !\n\nJ'ai noté votre message. {context_message} Utilisez les boutons pour continuer.",
                    buttons=[
                        {"title": "🔄 Retour au menu", "payload": "/go_back_greet_with_name"},
                        {"title": "📞 Support", "payload": "/ask_support"}
                    ]
                )
        
        return []


class ActionSmartFallback(Action):
    """Fallback intelligent qui analyse le contexte"""
    def name(self) -> Text:
        return "action_smart_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_text = tracker.latest_message.get("text", "").strip().lower()
        platform = tracker.get_slot("platform")
        has_account = tracker.get_slot("has_account")
        nom = tracker.get_slot("nom") or "Utilisateur"
        
        print(f"DEBUG ActionSmartFallback: user_text='{user_text}', platform={platform}, has_account={has_account}")
        
        # Analyser les mots-clés pour deviner l'intention
        if any(word in user_text for word in ['oui', 'yes', 'ok', 'accord', 'confirme', 'd\'accord', 'daccord']):
            if has_account is None and platform:
                # Probable confirmation de possession de compte
                dispatcher.utter_message(
                    text="💡 Je pense que vous confirmez avoir un compte. Voulez-vous vérifier votre compte ?",
                    buttons=[
                        {"title": "✅ Oui, vérifier mon compte", "payload": "/confirm_has_account"},
                        {"title": "❌ Non, pas de compte", "payload": "/deny_has_account"},
                        {"title": "🏠 Retour menu", "payload": "/go_back_greet_with_name"}
                    ]
                )
                return []
        elif any(word in user_text for word in ['non', 'no', 'pas', 'aucun', 'jamais', 'rien']):
            if has_account is None and platform:
                # Probable dénégation de possession de compte
                dispatcher.utter_message(
                    text="💡 Je pense que vous n'avez pas de compte. Voulez-vous savoir comment en créer un ?",
                    buttons=[
                        {"title": "ℹ️ Comment créer un compte", "payload": "/ask_account_creation"},
                        {"title": "✅ En fait, j'ai un compte", "payload": "/confirm_has_account"},
                        {"title": "🏠 Retour menu", "payload": "/go_back_greet_with_name"}
                    ]
                )
                return []
        elif any(word in user_text for word in ['aide', 'help', 'support', 'problème', 'souci', 'assistance']):
            dispatcher.utter_message(response="utter_ask_support")
            return []
        elif any(word in user_text for word in ['merci', 'thanks', 'remercie', 'thank you']):
            dispatcher.utter_message(
                text=f"De rien {nom} ! 😊 Je suis là pour vous aider.",
                buttons=[
                    {"title": "🔄 Continuer", "payload": "/go_back_greet_with_name"},
                    {"title": "📞 Autre question", "payload": "/ask_support"}
                ]
            )
            return []
        elif any(word in user_text for word in ['salut', 'bonjour', 'bonsoir', 'hello', 'hi']):
            # Re-salutation
            dispatcher.utter_message(
                text=f"Salut {nom} ! 👋 Je suis toujours là pour vous aider.",
                buttons=[
                    {"title": "🔄 Retour au menu", "payload": "/go_back_greet_with_name"},
                    {"title": "📞 Support", "payload": "/ask_support"}
                ]
            )
            return []
        
        # Fallback général avec suggestion de boutons
        dispatcher.utter_message(
            text=f"🤔 Désolé {nom}, je n'ai pas compris \"{user_text}\".\n\n💡 **Conseil** : Utilisez les boutons pour une navigation plus facile et éviter les malentendus !",
            buttons=[
                {"title": "🏠 Menu principal", "payload": "/go_back_greet_with_name"},
                {"title": "📞 Support", "payload": "/ask_support"}
            ]
        )
        
        return []