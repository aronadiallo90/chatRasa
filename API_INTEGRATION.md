# Préparation de l'intégration API

Le chatbot appelle désormais le backend au travers de `actions/backend_api.py`.
Les actions Rasa n'ont pas à connaître les URLs, jetons ou détails des bases.

## Mise en service

1. Définir dans l'environnement du serveur d'actions les variables de
   `.env.example` (`rasa run actions` ne lit pas de fichier `.env`).
2. Renseigner un jeton distinct pour chaque plateforme dans
   `CHATBOT_ECARRIERE_TOKEN` et `CHATBOT_PGDE_TOKEN`.
3. Mettre à jour les variables `*_ENDPOINT` si les chemins diffèrent.
4. Tester les six cas du contrat : agent E-Carrière, actes, projets, reset
   E-Carrière, compte PGDE et reset PGDE.

Les réponses attendues suivent l'enveloppe de `CONTRAT_INTERFACE_BACKEND.md`.
E-Carrière et PGDE sont isolés : une URL, un jeton et des chemins d'endpoint
peuvent être différents pour chaque plateforme.

## PGDE (backend Laravel `emplois`) — disponible

| Service | Méthode et URL |
|---|---|
| Vérification de compte | `POST {CHATBOT_PGDE_BASE_URL}/pgde/accounts/verify` |
| Réinitialisation du mot de passe | `POST {CHATBOT_PGDE_BASE_URL}/pgde/password/reset` |

- `CHATBOT_PGDE_BASE_URL` = `https://<domaine-pgde>/api/v1/chatbot`
- Authentification : `Authorization: Bearer <CHATBOT_PGDE_TOKEN>`, identique à
  `CHATBOT_API_TOKEN` côté Laravel (liste blanche d'IP optionnelle :
  `CHATBOT_ALLOWED_IPS`).
- Limites : 10 vérifications par minute et par CNI, 3 réinitialisations par
  15 minutes et par CNI, 120 appels par minute pour le serveur d'actions.

## Gestion des codes dans le chatbot

| Code | Comportement |
|---|---|
| `FOUND` | Données affichées |
| `INACTIVE_ACCOUNT` | Message « compte non activé » (le compte n'est pas masqué) |
| `NOT_FOUND`, `INVALID_INPUT` | Message « compte introuvable » |
| `RESET_ACCEPTED` | Confirmation d'envoi de l'email |
| `TOO_MANY_REQUESTS` | Reset : « demande déjà en cours » ; consultation : erreur temporaire |
| `UNAUTHORIZED`, `TEMPORARY_ERROR`, code inconnu, panne réseau, réponse non JSON | `BackendAPIError` → message « Problème temporaire » |

Aucun accès direct à SQL Server ou MySQL n'est effectué par le nouveau client.
