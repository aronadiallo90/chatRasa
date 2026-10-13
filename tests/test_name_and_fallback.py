"""Cas réels relevés en test (13/10) : saisie du nom, messages incompris, « 1 » au menu."""
import unittest

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions.actions import (
    ActionAskNameAgain,
    ActionFallbackMenu,
    ActionHandleFallbackAfterGreet,
    ActionHandleName,
    is_name_refusal,
    valid_name_or_none,
)


def _tracker(text, intent="nlu_fallback", slots=None, entities=None):
    return Tracker(
        "test", slots or {},
        {"text": text, "intent": {"name": intent}, "entities": entities or []},
        [{"event": "user", "text": text}], False, None, {}, "action_listen",
    )


def _slot_events(events):
    return {event["name"]: event["value"] for event in events if event.get("event") == "slot"}


class NameValidationTest(unittest.TestCase):
    def test_real_names_are_accepted(self):
        for name in ("Baba", "Philipe", "Upamecano", "Aïssatou", "Mame Diarra", "Jean-Pierre", "N'Diaye"):
            with self.subTest(name=name):
                self.assertEqual(valid_name_or_none(name), name)

    def test_digits_symbols_and_single_letters_are_rejected(self):
        for text in ("1", "g", "dfokn,gb", "1765200100341", "762230D", "a b c d e", "!!!"):
            with self.subTest(text=text):
                self.assertIsNone(valid_name_or_none(text))

    def test_refusal_does_not_catch_names_containing_pas_or_non(self):
        self.assertTrue(is_name_refusal("non"))
        self.assertTrue(is_name_refusal("je ne veux pas"))
        self.assertTrue(is_name_refusal("Je préfère pas"))
        self.assertFalse(is_name_refusal("Pascal"))
        self.assertFalse(is_name_refusal("Nana"))
        self.assertFalse(is_name_refusal("Nonna"))


class ActionHandleNameTest(unittest.TestCase):
    def test_new_name_replaces_the_previous_one(self):
        # Bug observé : « arona » saisi après « Baba » affichait « Bienvenue, Baba »
        dispatcher = CollectingDispatcher()

        events = ActionHandleName().run(dispatcher, _tracker("arona", "provide_name", {"nom": "Baba"}), {})

        self.assertEqual(_slot_events(events), {"nom": "Arona"})
        self.assertEqual(dispatcher.messages[0]["response"], "utter_greet_with_name")

    def test_entity_wins_over_full_sentence(self):
        entities = [{"entity": "nom", "value": "Waly"}]
        events = ActionHandleName().run(
            CollectingDispatcher(), _tracker("je m'appelle Waly", "provide_name", entities=entities), {})

        self.assertEqual(_slot_events(events), {"nom": "Waly"})

    def test_refusal_continues_without_name(self):
        dispatcher = CollectingDispatcher()

        events = ActionHandleName().run(dispatcher, _tracker("non", "refuse_name"), {})

        self.assertEqual(_slot_events(events), {"nom": "Utilisateur"})
        self.assertEqual(len(dispatcher.messages[0]["buttons"]), 3)

    def test_invalid_text_asks_again_without_setting_a_name(self):
        events = ActionHandleName().run(CollectingDispatcher(), _tracker("dfokn,gb"), {})

        # Pas de nom enregistré ; la nouvelle demande passe par une action dédiée (règle suivante)
        self.assertEqual(events, [{"event": "followup", "timestamp": None, "name": "action_ask_name_again"}])

    def test_ask_name_again_explains_what_is_expected(self):
        dispatcher = CollectingDispatcher()

        ActionAskNameAgain().run(dispatcher, _tracker("dfokn,gb"), {})

        self.assertIn("Je n'ai pas reconnu de nom", dispatcher.messages[0]["text"])
        self.assertIn("« non »", dispatcher.messages[0]["text"])

    def test_french_and_international_names_are_accepted(self):
        for typed, expected in (("pierre", "Pierre"), ("Sophie Martin", "Sophie Martin"),
                                ("élodie", "Élodie"), ("Kwame Mensah", "Kwame Mensah")):
            with self.subTest(typed=typed):
                events = ActionHandleName().run(CollectingDispatcher(), _tracker(typed), {})
                self.assertEqual(_slot_events(events), {"nom": expected})


class ActionHandleFallbackAfterGreetTest(unittest.TestCase):
    def test_unknown_word_after_name_question_is_taken_as_the_name(self):
        # Bug observé : « upamecano », « philipe » relançaient la demande de nom en boucle
        dispatcher = CollectingDispatcher()

        events = ActionHandleFallbackAfterGreet().run(dispatcher, _tracker("upamecano"), {})

        self.assertEqual(_slot_events(events), {"nom": "Upamecano"})
        self.assertEqual(dispatcher.messages[0]["response"], "utter_greet_with_name")


class ActionFallbackMenuTest(unittest.TestCase):
    def test_never_silent_and_offers_useful_choices(self):
        dispatcher = CollectingDispatcher()

        ActionFallbackMenu().run(dispatcher, _tracker("sdss", slots={"platform": "E-Carrière", "nom": "Baba"}), {})

        self.assertIn("Je n'ai pas bien compris", dispatcher.messages[0]["text"])
        payloads = [button["payload"] for button in dispatcher.messages[0]["buttons"]]
        self.assertEqual(payloads, ["/go_back_ecarriere", "/go_back_greet_with_name", "/ask_support"])

    def test_without_name_the_platforms_are_offered(self):
        dispatcher = CollectingDispatcher()

        ActionFallbackMenu().run(dispatcher, _tracker("1"), {})

        payloads = [button["payload"] for button in dispatcher.messages[0]["buttons"]]
        self.assertIn('/choose_platform{"platform": "PGDE"}', payloads)
        self.assertEqual(payloads[-1], "/ask_support")


if __name__ == "__main__":
    unittest.main()
