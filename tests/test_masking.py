"""Données personnelles affichées par Amath : toujours masquées (une CNI suffit à les demander)."""
import unittest
from unittest.mock import patch

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions import actions
from actions.actions import mask_email, mask_identifier, mask_person_name


class MaskingHelpersTest(unittest.TestCase):
    def test_username_keeps_only_its_ends(self):
        self.assertEqual(mask_identifier("Lalaaicha02"), "La•••••••02")

    def test_dossier_number(self):
        self.assertEqual(mask_identifier("258706"), "25••06")
        self.assertEqual(mask_identifier(258706), "25••06")

    def test_short_and_empty_values(self):
        self.assertEqual(mask_identifier("abc"), "a••")
        self.assertEqual(mask_identifier(None), "")

    def test_email_hides_the_local_part(self):
        self.assertEqual(mask_email("mbaye.dieng@fpublique.gouv.sn"), "mb•••@fpublique.gouv.sn")
        self.assertEqual(mask_email(None), "")

    def test_name_shows_first_name_and_initial(self):
        self.assertEqual(mask_person_name("Arona Dia DIALLO"), "Arona D.")
        self.assertEqual(mask_person_name("Aliou"), "Aliou")


class VerifiedPgdeAccountTest(unittest.TestCase):
    def test_verified_account_message_never_contains_raw_data(self):
        account = {"code": "FOUND", "id": 258706, "nom": "Aïcha LALA", "username": "Lalaaicha02",
                   "email": "aicha.lala@exemple.sn", "cni": "1934200001259", "actif": True}
        tracker = Tracker(
            "test", {"platform": "PGDE", "has_account": "Oui"},
            {"text": "1934200001259", "intent": {"name": "provide_cni"}, "entities": []},
            [], False, None, {}, "action_listen",
        )
        dispatcher = CollectingDispatcher()

        with patch.object(actions.PGDEAPIService, "verify_user_by_cni", return_value=account):
            actions.ActionHandleCNI().run(dispatcher, tracker, {})

        shown = [message for message in dispatcher.messages if message.get("response") == "utter_account_verified"]
        self.assertTrue(shown, dispatcher.messages)
        values = " ".join(str(value) for value in shown[0].values())
        for raw in ("Lalaaicha02", "258706", "LALA", "aicha.lala@"):
            self.assertNotIn(raw, values)
        self.assertEqual(shown[0]["username"], "La•••••••02")


if __name__ == "__main__":
    unittest.main()
