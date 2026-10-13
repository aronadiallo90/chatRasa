"""Anti-énumération : au plus 5 CNI vérifiées par conversation."""
import unittest
from unittest.mock import patch

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions import actions
from actions.actions import MAX_CNI_ATTEMPTS_PER_CONVERSATION, looks_like_cni


def _tracker(text, attempts=None, platform="PGDE"):
    slots = {"platform": platform, "has_account": "Oui", "cni_attempts": attempts}
    return Tracker("test", slots, {"text": text, "intent": {"name": "provide_cni"}, "entities": []},
                   [], False, None, {}, "action_listen")


def _attempts(events):
    return next((event["value"] for event in events if event.get("name") == "cni_attempts"), None)


class LooksLikeCniTest(unittest.TestCase):
    def test_same_rule_as_the_laravel_relay(self):
        self.assertTrue(looks_like_cni("1934200001259"))
        self.assertTrue(looks_like_cni("1934 2000 01259"))
        self.assertFalse(looks_like_cni("762230D"))
        self.assertFalse(looks_like_cni("Martin"))
        self.assertFalse(looks_like_cni("12345"))


class CniAttemptLimitTest(unittest.TestCase):
    def setUp(self):
        patcher = patch.object(actions.PGDEAPIService, "verify_user_by_cni", return_value=None)
        self.verify = patcher.start()
        self.addCleanup(patcher.stop)

    def test_attempts_are_counted_and_verified_below_the_limit(self):
        events = actions.ActionHandleCNI().run(CollectingDispatcher(), _tracker("1934200001259", attempts=2), {})

        self.assertEqual(_attempts(events), 3)
        self.verify.assert_called_once_with("1934200001259")

    def test_attempt_over_the_limit_is_refused_without_calling_the_backend(self):
        dispatcher = CollectingDispatcher()

        events = actions.ActionHandleCNI().run(
            dispatcher, _tracker("1934200001259", attempts=MAX_CNI_ATTEMPTS_PER_CONVERSATION), {})

        self.verify.assert_not_called()
        self.assertEqual(_attempts(events), MAX_CNI_ATTEMPTS_PER_CONVERSATION + 1)
        self.assertIn("Nombre maximal de vérifications", dispatcher.messages[0]["text"])
        self.assertEqual(dispatcher.messages[0]["buttons"][0]["payload"], "/ask_support")

    def test_matricule_is_not_counted_as_a_cni(self):
        events = actions.ActionHandleMatricule().run(
            CollectingDispatcher(), _tracker("762230D", attempts=MAX_CNI_ATTEMPTS_PER_CONVERSATION, platform="E-Carrière"), {})

        self.assertIsNone(_attempts(events))


if __name__ == "__main__":
    unittest.main()
