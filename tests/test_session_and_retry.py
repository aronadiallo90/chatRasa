import os
import unittest
from unittest.mock import patch

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions.actions import ActionSessionStart, ActionStartAccountVerification


def _tracker(slots):
    return Tracker("test", slots, {"text": "", "intent": {"name": "start_account_verification"}, "entities": []},
                   [], False, None, {}, "action_listen")


class ActionSessionStartTest(unittest.TestCase):
    def test_only_platform_and_name_survive_a_new_session(self):
        tracker = _tracker({
            "platform": "PGDE", "nom": "Arona",
            "cni": "1934200001259", "email": "a@exemple.sn", "nom_officiel": "Arona Dia", "agent_id": "42",
        })

        events = ActionSessionStart().run(CollectingDispatcher(), tracker, {})

        self.assertEqual(events[0]["event"], "session_started")
        kept = {event["name"]: event["value"] for event in events if event["event"] == "slot"}
        kept.pop("ministere")
        self.assertEqual(kept, {"platform": "PGDE", "nom": "Arona"})
        self.assertEqual((events[-1]["event"], events[-1]["name"]), ("action", "action_listen"))

    def test_nothing_to_keep_on_a_fresh_conversation(self):
        events = ActionSessionStart().run(CollectingDispatcher(), _tracker({}), {})

        slots = [event["name"] for event in events if event["event"] == "slot"]
        self.assertEqual(slots, ["ministere"])


class MinistereNameTest(unittest.TestCase):
    def _ministere(self):
        events = ActionSessionStart().run(CollectingDispatcher(), _tracker({}), {})
        return next(event["value"] for event in events if event.get("name") == "ministere")

    def test_default_name_is_the_current_ministry(self):
        with patch.dict(os.environ, {"CHATBOT_MINISTERE_NOM": ""}):
            self.assertEqual(
                self._ministere(),
                "Ministère de la Fonction publique, du Travail et de la Réforme du Service public",
            )

    def test_name_comes_from_the_environment(self):
        with patch.dict(os.environ, {"CHATBOT_MINISTERE_NOM": "  Ministère de Test  "}):
            self.assertEqual(self._ministere(), "Ministère de Test")


class ActionStartAccountVerificationTest(unittest.TestCase):
    def test_lost_platform_asks_for_the_platform_again(self):
        dispatcher = CollectingDispatcher()

        events = ActionStartAccountVerification().run(dispatcher, _tracker({"platform": None}), {})

        self.assertEqual(events, [])
        self.assertIn("Pour quelle plateforme", dispatcher.messages[0]["text"])
        payloads = [button["payload"] for button in dispatcher.messages[0]["buttons"]]
        self.assertIn('/choose_platform{"platform": "PGDE"}', payloads)
        self.assertEqual(len(payloads), 3)

    def test_known_platform_keeps_the_usual_question(self):
        dispatcher = CollectingDispatcher()

        events = ActionStartAccountVerification().run(dispatcher, _tracker({"platform": "PGDE"}), {})

        self.assertEqual(dispatcher.messages[0]["response"], "utter_ask_has_account")
        self.assertIn({"event": "slot", "timestamp": None, "name": "cni", "value": None}, events)


if __name__ == "__main__":
    unittest.main()
