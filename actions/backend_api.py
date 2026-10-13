"""Client HTTP du backend métier du chatbot.

Ce module est l'unique point d'accès aux données E-Carrière et PGDE. Il ne
contient ni identifiant de base de données ni requête SQL.
"""

import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


LOGGER = logging.getLogger(__name__)

# Codes métier du contrat (CONTRAT_INTERFACE_BACKEND.md).
CODE_FOUND = "FOUND"
CODE_NOT_FOUND = "NOT_FOUND"
CODE_INVALID_INPUT = "INVALID_INPUT"
CODE_INACTIVE_ACCOUNT = "INACTIVE_ACCOUNT"
CODE_RESET_ACCEPTED = "RESET_ACCEPTED"
CODE_TOO_MANY_REQUESTS = "TOO_MANY_REQUESTS"

# Codes qui décrivent un résultat métier exploitable par la conversation.
# Tout autre code (UNAUTHORIZED, TEMPORARY_ERROR, code inconnu) est une panne.
FUNCTIONAL_CODES = {
    CODE_FOUND,
    CODE_NOT_FOUND,
    CODE_INVALID_INPUT,
    CODE_INACTIVE_ACCOUNT,
    CODE_RESET_ACCEPTED,
    CODE_TOO_MANY_REQUESTS,
}


class BackendAPIError(Exception):
    """Erreur contrôlée lors d'un appel au backend (panne, refus, hors contrat)."""

    def __init__(self, message: str, code: Optional[str] = None,
                 correlation_id: Optional[str] = None) -> None:
        super().__init__(message)
        self.code = code
        self.correlation_id = correlation_id


@dataclass
class BackendResponse:
    success: bool
    code: str
    message: str
    data: Optional[Dict[str, Any]]
    correlation_id: Optional[str] = None


class BackendAPIClient:
    """Client du contrat défini dans CONTRAT_INTERFACE_BACKEND.md."""

    def __init__(self, base_url_variable: str, token_variable: str) -> None:
        self.base_url_variable = base_url_variable
        self.base_url = os.getenv(base_url_variable, "").rstrip("/")
        self.timeout = float(os.getenv("CHATBOT_BACKEND_TIMEOUT", "15"))
        self.token = os.getenv(token_variable)

    def post(self, endpoint: str, payload: Dict[str, Any]) -> BackendResponse:
        if not self.base_url:
            raise BackendAPIError(f"{self.base_url_variable} n'est pas configurée")

        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        try:
            response = requests.post(
                f"{self.base_url}{endpoint}", json=payload, headers=headers,
                timeout=self.timeout,
            )
            body = response.json()
        except requests.RequestException as error:
            raise BackendAPIError("Backend indisponible") from error
        except ValueError as error:
            raise BackendAPIError("Réponse backend invalide") from error

        if not isinstance(body, dict) or "success" not in body or "code" not in body:
            raise BackendAPIError("Réponse backend hors contrat")

        result = BackendResponse(
            success=bool(body["success"]),
            code=str(body["code"]),
            message=str(body.get("message", "")),
            data=body.get("data"),
            correlation_id=body.get("correlation_id"),
        )

        if result.code not in FUNCTIONAL_CODES:
            LOGGER.warning(
                "Appel backend %s refusé : code=%s correlation_id=%s",
                endpoint, result.code, result.correlation_id,
            )
            raise BackendAPIError(result.message or "Erreur backend", result.code, result.correlation_id)

        return result


def format_items(items: Any, label: str) -> list[str]:
    """Transforme les objets du contrat en texte compatible avec les actions Rasa."""
    formatted = []
    for index, item in enumerate(items or [], start=1):
        if not isinstance(item, dict):
            continue
        text = f"**{index}. {label} n°{item.get('numero') or 'Sans numéro'}**"
        if item.get("type"):
            text += f"\nType : {item['type']}"
        if item.get("etat"):
            text += f"\nÉtat : {item['etat']}"
        if item.get("date"):
            # Le backend renvoie une date ISO ; l'interface affiche JJ/MM/AAAA.
            date = str(item["date"])
            try:
                yyyy, mm, dd = date[:10].split("-")
                date = f"{dd}/{mm}/{yyyy}"
            except ValueError:
                pass
            text += f"\nDate : {date}"
        formatted.append(text)
    return formatted


def _full_name(account: Dict[str, Any]) -> str:
    return account.get("nom_complet") or " ".join(filter(None, [account.get("prenom"), account.get("nom")]))


def _reject_throttled(result: BackendResponse) -> None:
    """Une consultation limitée en débit est traitée comme une indisponibilité temporaire."""
    if result.code == CODE_TOO_MANY_REQUESTS:
        raise BackendAPIError(result.message, result.code, result.correlation_id)


class ECarriereBackendService:
    def __init__(self, client: Optional[BackendAPIClient] = None) -> None:
        self.client = client or BackendAPIClient(
            "CHATBOT_ECARRIERE_BASE_URL", "CHATBOT_ECARRIERE_TOKEN"
        )

    def verify_user_by_cni_matricule(self, cni: str, matricule: str) -> Optional[Dict[str, Any]]:
        """Retourne l'agent (avec `code`), ou None si aucune correspondance."""
        result = self.client.post(
            os.getenv("CHATBOT_ECARRIERE_VERIFY_ENDPOINT", "/ecarriere/agents/verify"),
            {"cni": cni, "matricule": matricule},
        )
        _reject_throttled(result)
        if result.code not in (CODE_FOUND, CODE_INACTIVE_ACCOUNT) or not result.data:
            return None
        agent = result.data
        return {
            "code": result.code,
            "id": agent.get("agent_id"),
            "nom": _full_name(agent),
            "matricule": agent.get("matricule"),
            "cni": agent.get("cni"),
            "email": agent.get("email"),
            "projets": format_items(agent.get("projets"), "Projet"),
            # Le contrat ne définit pas encore l'activation E-Carrière : actif sauf INACTIVE_ACCOUNT.
            "actif": result.code == CODE_FOUND and agent.get("actif", True),
        }

    def verify_user_by_cni(self, cni: str) -> Optional[Dict[str, Any]]:
        # Le contrat vérifie le couple CNI + matricule. Cette étape ne fait donc
        # volontairement aucun appel : elle conserve simplement la CNI jusqu'à la
        # saisie du matricule, moment où verify_user_by_cni_matricule est appelé.
        return {"cni": cni}

    def get_all_actes(self, agent_id: str) -> Optional[Dict[str, Any]]:
        result = self.client.post(
            os.getenv("CHATBOT_ECARRIERE_ACTES_ENDPOINT", "/ecarriere/agents/actes"),
            {"agent_id": agent_id},
        )
        _reject_throttled(result)
        if not result.success:
            return None
        return {"actes": format_items((result.data or {}).get("actes"), "Acte")}

    def get_projets(self, agent_id: str) -> Optional[Dict[str, Any]]:
        result = self.client.post(
            os.getenv("CHATBOT_ECARRIERE_PROJETS_ENDPOINT", "/ecarriere/agents/projets"),
            {"agent_id": agent_id},
        )
        _reject_throttled(result)
        if not result.success:
            return None
        return {"projets": format_items((result.data or {}).get("projets"), "Projet")}

    def request_password_reset_ecarriere(self, email: str) -> str:
        """Retourne le code métier (RESET_ACCEPTED en cas de succès)."""
        result = self.client.post(
            os.getenv("CHATBOT_ECARRIERE_RESET_ENDPOINT", "/ecarriere/password/reset"),
            {"email": email},
        )
        return result.code


ECARRIERE_MODES = ("legacy", "api")


def build_ecarriere_service() -> Any:
    """Choisit la source E-Carrière selon CHATBOT_ECARRIERE_MODE.

    legacy (défaut) : lecture directe SQL Server, tant que l'API E-Carrière n'existe pas.
    api             : client HTTP du contrat backend.
    Une valeur inconnue fait échouer le démarrage plutôt que de choisir en silence.
    """
    mode = os.getenv("CHATBOT_ECARRIERE_MODE", "legacy").strip().lower()
    if mode not in ECARRIERE_MODES:
        raise ValueError(f"CHATBOT_ECARRIERE_MODE invalide : {mode!r} (attendu : legacy ou api)")

    LOGGER.info("Source E-Carrière : %s", mode)
    if mode == "api":
        return ECarriereBackendService()

    # Import local : le module legacy dépend de pymssql et importe déjà ce module.
    from .ecarriere_legacy import LegacyECarriereService
    return LegacyECarriereService()


class PGDEBackendService:
    def __init__(self, client: Optional[BackendAPIClient] = None) -> None:
        self.client = client or BackendAPIClient("CHATBOT_PGDE_BASE_URL", "CHATBOT_PGDE_TOKEN")

    def verify_user_by_cni(self, cni: str) -> Optional[Dict[str, Any]]:
        """Retourne le compte (avec `code` et `actif`), ou None si aucun compte.

        Un compte inactif est retourné avec code=INACTIVE_ACCOUNT et actif=False
        pour que la conversation puisse l'expliquer à l'utilisateur.
        """
        result = self.client.post(
            os.getenv("CHATBOT_PGDE_VERIFY_ENDPOINT", "/pgde/accounts/verify"), {"cni": cni}
        )
        _reject_throttled(result)
        if result.code not in (CODE_FOUND, CODE_INACTIVE_ACCOUNT):
            return None
        account = result.data or {}
        return {
            "code": result.code,
            "id": account.get("user_id") or account.get("numero_dossier"),
            "nom": _full_name(account),
            "username": account.get("username"),
            "email": account.get("email"),
            "cni": account.get("cni") or cni,
            "actif": result.code == CODE_FOUND and bool(account.get("actif", True)),
        }

    def request_password_reset(self, cni: str, email: str) -> str:
        """Retourne le code métier (RESET_ACCEPTED, NOT_FOUND, INACTIVE_ACCOUNT, TOO_MANY_REQUESTS...)."""
        result = self.client.post(
            os.getenv("CHATBOT_PGDE_RESET_ENDPOINT", "/pgde/password/reset"),
            {"cni": cni, "email": email},
        )
        return result.code
