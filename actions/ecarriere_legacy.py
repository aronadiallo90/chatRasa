"""Accès E-Carrière historique (lecture directe SQL Server).

Utilisé tant que l'API E-Carrière n'existe pas (CHATBOT_ECARRIERE_MODE=legacy).
Expose la même interface que ECarriereBackendService : les actions Rasa ne
savent pas quel mode est actif.
"""

import logging
import os
from datetime import date, datetime
from typing import Any, Dict, List, Optional
from urllib.parse import quote

import pymssql
import requests
import urllib3

from .backend_api import CODE_FOUND, CODE_RESET_ACCEPTED, BackendAPIError, format_items


LOGGER = logging.getLogger(__name__)

# Règle métier historique : un agent rattaché à cette affectation a activé son compte.
ACTIVATED_AFFECTATION_ID = 174200
CODE_RESET_REFUSED = "RESET_REFUSED"
DEFAULT_RESET_URL = "https://e-carriere.sec.gouv.sn/account-management-fudpe/users/{email}/reset-password-forgot"

AGENT_COLUMNS = "agt_id, agt_cni, agt_matricule_solde, agt_nom, agt_prenom, agt_affectation_id, agt_email"

PROJETS_QUERY = """
    SELECT TOP 3 ac.act_numero_projet, ta.tac_libelle, ea.eta_act_libelle, ac.act_date_projet
    FROM referentiel_fudpe_new.dbo.acte_agent aa
    INNER JOIN referentiel_fudpe_new.dbo.acte ac ON ac.act_id = aa.act_agt_act_id
    LEFT JOIN referentiel_fudpe_new.dbo.etat_acte ea ON ea.eta_act_id = ac.act_etat_id
    LEFT JOIN referentiel_fudpe_new.dbo.type_acte ta ON ta.tac_id = ac.act_tac_id
    WHERE aa.act_agt_agt_id = %s AND ac.act_is_projet = 1
    ORDER BY ac.act_date_projet DESC
"""

# Actes validés (état 24) et datés uniquement, comme dans la version en production.
ACTES_QUERY = """
    SELECT TOP 3 ac.act_numero_acte, ta.tac_libelle, ea.eta_act_libelle, ac.act_date_acte
    FROM referentiel_fudpe_new.dbo.acte_agent aa
    INNER JOIN referentiel_fudpe_new.dbo.acte ac ON ac.act_id = aa.act_agt_act_id
    LEFT JOIN referentiel_fudpe_new.dbo.etat_acte ea ON ea.eta_act_id = ac.act_etat_id
    LEFT JOIN referentiel_fudpe_new.dbo.type_acte ta ON ta.tac_id = ac.act_tac_id
    WHERE aa.act_agt_agt_id = %s AND ac.act_is_projet = 0
      AND ac.act_etat_id = 24 AND ac.act_date_acte IS NOT NULL
    ORDER BY ac.act_date_acte DESC
"""


def _iso_date(value: Any) -> Optional[str]:
    if isinstance(value, (datetime, date)):
        return value.strftime("%Y-%m-%d")
    return None


class LegacyECarriereService:
    """Même contrat que ECarriereBackendService, alimenté par SQL Server."""

    def _connect(self) -> Any:
        host = os.getenv("LEGACY_ECARRIERE_DB_HOST", "")
        if not host:
            raise BackendAPIError("LEGACY_ECARRIERE_DB_HOST n'est pas configurée")
        try:
            return pymssql.connect(
                server=host,
                port=int(os.getenv("LEGACY_ECARRIERE_DB_PORT", "1433")),
                database=os.getenv("LEGACY_ECARRIERE_DB_NAME", ""),
                user=os.getenv("LEGACY_ECARRIERE_DB_USER", ""),
                password=os.getenv("LEGACY_ECARRIERE_DB_PASSWORD", ""),
                timeout=30,
                login_timeout=30,
            )
        except pymssql.Error as error:
            raise BackendAPIError("Base E-Carrière indisponible") from error

    def _fetch(self, query: str, params: tuple, fetch_all: bool) -> Any:
        connection = self._connect()
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            return cursor.fetchall() if fetch_all else cursor.fetchone()
        except pymssql.Error as error:
            raise BackendAPIError("Erreur de lecture E-Carrière") from error
        finally:
            connection.close()

    def _find_agent(self, where: str, params: tuple) -> Optional[tuple]:
        query = (
            f"SELECT {AGENT_COLUMNS} FROM referentiel_fudpe_new.dbo.agent "
            f"WHERE {where} AND agt_deleted = 0"
        )
        return self._fetch(query, params, fetch_all=False)

    def _items(self, query: str, agent_id: Any, label: str) -> List[str]:
        rows = self._fetch(query, (agent_id,), fetch_all=True) or []
        items = [
            {"numero": numero, "type": type_libelle, "etat": etat, "date": _iso_date(item_date)}
            for numero, type_libelle, etat, item_date in rows
        ]
        return format_items(items, label)

    def verify_user_by_cni(self, cni: str) -> Optional[Dict[str, Any]]:
        agent = self._find_agent("agt_cni = %s", (cni,))
        if not agent:
            return None
        agent_id, agent_cni, matricule, nom, prenom, _, _ = agent
        return {"id": agent_id, "nom": f"{prenom} {nom}", "matricule": matricule, "cni": agent_cni}

    def verify_user_by_cni_matricule(self, cni: str, matricule: str) -> Optional[Dict[str, Any]]:
        agent = self._find_agent("agt_cni = %s AND agt_matricule_solde = %s", (cni, matricule))
        if not agent:
            return None
        agent_id, agent_cni, matricule_solde, nom, prenom, affectation_id, email = agent
        return {
            "code": CODE_FOUND,
            "id": agent_id,
            "nom": f"{prenom} {nom}",
            "matricule": matricule_solde,
            "cni": agent_cni,
            "email": email,
            "projets": self._items(PROJETS_QUERY, agent_id, "Projet"),
            "actif": affectation_id == ACTIVATED_AFFECTATION_ID,
        }

    def get_projets(self, agent_id: str) -> Optional[Dict[str, Any]]:
        return {"projets": self._items(PROJETS_QUERY, agent_id, "Projet")}

    def get_all_actes(self, agent_id: str) -> Optional[Dict[str, Any]]:
        return {"actes": self._items(ACTES_QUERY, agent_id, "Acte")}

    def request_password_reset_ecarriere(self, email: str) -> str:
        """Appelle le service officiel E-Carrière (certificat auto-signé, d'où verify=False)."""
        reset_url = os.getenv("LEGACY_ECARRIERE_RESET_URL", DEFAULT_RESET_URL).format(
            email=quote(email, safe="@")
        )
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        try:
            response = requests.put(
                reset_url, headers={"Accept": "application/json"}, timeout=15, verify=False
            )
        except requests.RequestException as error:
            raise BackendAPIError("Service de réinitialisation E-Carrière indisponible") from error

        if response.status_code != 200:
            LOGGER.warning("Reset E-Carrière refusé : HTTP %s", response.status_code)
            return CODE_RESET_REFUSED
        return CODE_RESET_ACCEPTED
