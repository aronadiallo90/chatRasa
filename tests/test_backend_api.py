import os
import unittest
from unittest.mock import Mock, patch

import requests

from actions.backend_api import (
    BackendAPIClient,
    BackendAPIError,
    BackendResponse,
    ECarriereBackendService,
    PGDEBackendService,
)


def _client_returning(code: str, data=None, success=None) -> Mock:
    """Client factice qui renvoie une réponse conforme au contrat."""
    client = Mock()
    client.post.return_value = BackendResponse(
        success=code in ("FOUND", "RESET_ACCEPTED") if success is None else success,
        code=code,
        message="",
        data=data,
    )
    return client


def _http_response(body) -> Mock:
    response = Mock()
    response.json.return_value = body
    return response


class BackendAPIClientTest(unittest.TestCase):
    def setUp(self):
        patcher = patch.dict(os.environ, {"CHATBOT_PGDE_BASE_URL": "http://pgde.test/api/v1/chatbot"})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.client = BackendAPIClient("CHATBOT_PGDE_BASE_URL", "CHATBOT_PGDE_TOKEN")

    def test_missing_backend_url_is_a_controlled_error(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(BackendAPIError):
                BackendAPIClient("CHATBOT_PGDE_BASE_URL", "CHATBOT_PGDE_TOKEN").post("/accounts/verify", {"cni": "123"})

    @patch("actions.backend_api.requests.post", side_effect=requests.ConnectionError())
    def test_unreachable_backend_is_a_controlled_error(self, _post):
        with self.assertRaises(BackendAPIError):
            self.client.post("/pgde/accounts/verify", {"cni": "123"})

    @patch("actions.backend_api.requests.post")
    def test_non_json_response_is_a_controlled_error(self, post):
        post.return_value.json.side_effect = ValueError("HTML")
        with self.assertRaises(BackendAPIError):
            self.client.post("/pgde/accounts/verify", {"cni": "123"})

    @patch("actions.backend_api.requests.post")
    def test_technical_codes_raise_with_code_and_correlation_id(self, post):
        for code in ("UNAUTHORIZED", "TEMPORARY_ERROR", "service_unavailable"):
            post.return_value = _http_response(
                {"success": False, "code": code, "message": "x", "correlation_id": "abc123"}
            )
            with self.assertRaises(BackendAPIError) as raised:
                self.client.post("/pgde/accounts/verify", {"cni": "123"})
            self.assertEqual(raised.exception.code, code)
            self.assertEqual(raised.exception.correlation_id, "abc123")

    @patch("actions.backend_api.requests.post")
    def test_functional_code_is_returned(self, post):
        post.return_value = _http_response({"success": False, "code": "NOT_FOUND", "data": None})

        result = self.client.post("/pgde/accounts/verify", {"cni": "123"})

        self.assertEqual(result.code, "NOT_FOUND")


class ECarriereBackendServiceTest(unittest.TestCase):
    def test_response_is_adapted_to_rasa_format(self):
        client = _client_returning("FOUND", {
            "agent_id": "123", "nom_complet": "Aminata DIOP",
            "matricule": "123456A", "email": "a@example.sn",
            "projets": [{"numero": "PROJ-1", "date": "2026-06-15"}],
        })

        agent = ECarriereBackendService(client).verify_user_by_cni_matricule("123", "123456A")

        self.assertEqual(agent["id"], "123")
        self.assertTrue(agent["actif"])
        self.assertEqual(agent["projets"], ["**1. Projet n°PROJ-1**\n📅 Date : 15/06/2026"])

    def test_not_found_returns_none(self):
        client = _client_returning("NOT_FOUND")

        self.assertIsNone(ECarriereBackendService(client).verify_user_by_cni_matricule("123", "1A"))

    def test_reset_returns_business_code(self):
        client = _client_returning("RESET_ACCEPTED")

        self.assertEqual(ECarriereBackendService(client).request_password_reset_ecarriere("a@b.sn"), "RESET_ACCEPTED")


class PGDEBackendServiceTest(unittest.TestCase):
    ACCOUNT = {
        "user_id": "789", "numero_dossier": "789", "nom": "NDIAYE", "prenom": "Moussa",
        "nom_complet": "Moussa NDIAYE", "username": "mndiaye",
        "email": "moussa@exemple.sn", "cni": "1234567890123", "actif": True,
    }

    def test_active_account(self):
        account = PGDEBackendService(_client_returning("FOUND", self.ACCOUNT)).verify_user_by_cni("1234567890123")

        self.assertEqual(account["code"], "FOUND")
        self.assertEqual(account["id"], "789")
        self.assertEqual(account["nom"], "Moussa NDIAYE")
        self.assertTrue(account["actif"])

    def test_inactive_account_is_surfaced_not_hidden(self):
        inactive = dict(self.ACCOUNT, actif=False)

        account = PGDEBackendService(_client_returning("INACTIVE_ACCOUNT", inactive)).verify_user_by_cni("1234567890123")

        self.assertEqual(account["code"], "INACTIVE_ACCOUNT")
        self.assertFalse(account["actif"])

    def test_not_found_and_invalid_input_return_none(self):
        for code in ("NOT_FOUND", "INVALID_INPUT"):
            self.assertIsNone(PGDEBackendService(_client_returning(code)).verify_user_by_cni("1"))

    def test_throttled_verification_is_a_temporary_error(self):
        with self.assertRaises(BackendAPIError):
            PGDEBackendService(_client_returning("TOO_MANY_REQUESTS")).verify_user_by_cni("1234567890123")

    def test_reset_returns_business_code(self):
        for code in ("RESET_ACCEPTED", "NOT_FOUND", "INACTIVE_ACCOUNT", "TOO_MANY_REQUESTS"):
            service = PGDEBackendService(_client_returning(code))
            self.assertEqual(service.request_password_reset("1234567890123", "m@exemple.sn"), code)


if __name__ == "__main__":
    unittest.main()
