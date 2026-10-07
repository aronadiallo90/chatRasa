import os
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

import pymssql
import requests

from actions.backend_api import BackendAPIError, ECarriereBackendService, build_ecarriere_service
from actions.ecarriere_legacy import LegacyECarriereService

LEGACY_ENV = {"LEGACY_ECARRIERE_DB_HOST": "sql.test", "LEGACY_ECARRIERE_DB_NAME": "db"}
AGENT_ROW = (42, "1234567890123", "123456A", "DIOP", "Aminata", 174200, "a.diop@exemple.sn")


def _fake_connection(fetchone=None, fetchall=None) -> MagicMock:
    """Connexion pymssql factice : fetchone pour l'agent, fetchall pour projets/actes."""
    connection = MagicMock()
    cursor = connection.cursor.return_value
    cursor.fetchone.return_value = fetchone
    cursor.fetchall.return_value = fetchall or []
    return connection


class BuildECarriereServiceTest(unittest.TestCase):
    def test_legacy_is_the_default_mode(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertIsInstance(build_ecarriere_service(), LegacyECarriereService)

    def test_api_mode(self):
        with patch.dict(os.environ, {"CHATBOT_ECARRIERE_MODE": " API "}):
            self.assertIsInstance(build_ecarriere_service(), ECarriereBackendService)

    def test_unknown_mode_fails_fast(self):
        with patch.dict(os.environ, {"CHATBOT_ECARRIERE_MODE": "sql"}):
            with self.assertRaises(ValueError):
                build_ecarriere_service()


@patch.dict(os.environ, LEGACY_ENV)
class LegacyECarriereServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = LegacyECarriereService()

    @patch("actions.ecarriere_legacy.pymssql.connect")
    def test_verified_agent_matches_api_format(self, connect):
        connect.side_effect = [
            _fake_connection(fetchone=AGENT_ROW),
            _fake_connection(fetchall=[("P-1", "Avancement", "En cours", datetime(2026, 6, 15))]),
        ]

        agent = self.service.verify_user_by_cni_matricule("1234567890123", "123456A")

        self.assertEqual(agent["code"], "FOUND")
        self.assertEqual(agent["id"], 42)
        self.assertEqual(agent["nom"], "Aminata DIOP")
        self.assertEqual(agent["email"], "a.diop@exemple.sn")
        self.assertTrue(agent["actif"])
        self.assertEqual(
            agent["projets"],
            ["**1. Projet n°P-1**\n📋 Type : Avancement\n📊 État : En cours\n📅 Date : 15/06/2026"],
        )

    @patch("actions.ecarriere_legacy.pymssql.connect")
    def test_agent_outside_activated_affectation_is_inactive(self, connect):
        inactive_row = AGENT_ROW[:5] + (999,) + AGENT_ROW[6:]
        connect.side_effect = [_fake_connection(fetchone=inactive_row), _fake_connection()]

        agent = self.service.verify_user_by_cni_matricule("1234567890123", "123456A")

        self.assertFalse(agent["actif"])
        self.assertEqual(agent["projets"], [])

    @patch("actions.ecarriere_legacy.pymssql.connect")
    def test_unknown_agent_returns_none(self, connect):
        connect.return_value = _fake_connection(fetchone=None)

        self.assertIsNone(self.service.verify_user_by_cni_matricule("1", "1A"))
        self.assertIsNone(self.service.verify_user_by_cni("1"))

    @patch("actions.ecarriere_legacy.pymssql.connect", side_effect=pymssql.OperationalError("down"))
    def test_database_down_is_a_backend_error(self, _connect):
        with self.assertRaises(BackendAPIError):
            self.service.get_all_actes(42)

    def test_missing_host_is_a_backend_error(self):
        with patch.dict(os.environ, {"LEGACY_ECARRIERE_DB_HOST": ""}):
            with self.assertRaises(BackendAPIError):
                self.service.verify_user_by_cni("1")

    @patch("actions.ecarriere_legacy.pymssql.connect")
    def test_actes_are_formatted_and_connection_closed(self, connect):
        connection = _fake_connection(fetchall=[("A-9", "Titularisation", "Validé", datetime(2024, 1, 10))])
        connect.return_value = connection

        actes = self.service.get_all_actes(42)

        self.assertEqual(actes["actes"], ["**1. Acte n°A-9**\n📋 Type : Titularisation\n📊 État : Validé\n📅 Date : 10/01/2024"])
        connection.close.assert_called_once()

    @patch("actions.ecarriere_legacy.requests.put")
    def test_reset_codes(self, put):
        put.return_value.status_code = 200
        self.assertEqual(self.service.request_password_reset_ecarriere("a.diop@exemple.sn"), "RESET_ACCEPTED")
        self.assertIn("/users/a.diop@exemple.sn/reset-password-forgot", put.call_args.args[0])

        put.return_value.status_code = 404
        self.assertEqual(self.service.request_password_reset_ecarriere("a.diop@exemple.sn"), "RESET_REFUSED")

    @patch("actions.ecarriere_legacy.requests.put", side_effect=requests.ConnectionError())
    def test_reset_service_down_is_a_backend_error(self, _put):
        with self.assertRaises(BackendAPIError):
            self.service.request_password_reset_ecarriere("a.diop@exemple.sn")


if __name__ == "__main__":
    unittest.main()
