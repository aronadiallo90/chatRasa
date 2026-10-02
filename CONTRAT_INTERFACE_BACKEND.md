# Contrat d'interface Backend — Chatbot Amath

## But

Ce document définit les données que le backend doit recevoir et retourner au chatbot. Le développeur backend reste libre de choisir les URLs, les méthodes HTTP et l'architecture interne.

Le chatbot ne doit avoir aucun accès direct aux bases E-Carrière (SQL Server) et PGDE (MySQL).

## Règles générales

- Tous les échanges sont sécurisés par HTTPS et une authentification convenue ensemble.
- Les requêtes et réponses sont au format JSON.
- Les dates sont retournées au format ISO `YYYY-MM-DD`.
- Les listes de projets et d'actes sont limitées aux trois éléments les plus récents, triés du plus récent au plus ancien.
- Les mots de passe, secrets et informations de connexion aux bases ne doivent jamais être retournés.
- Les exemples ci-dessous illustrent le contrat ; les données sont fictives.

## Format de réponse commun

Chaque réponse doit permettre au chatbot de connaître le résultat de l'opération.

```json
{
  "success": true,
  "code": "FOUND",
  "message": "Agent trouvé",
  "data": {},
  "correlation_id": "a1b2c3d4"
}
```

`correlation_id` est facultatif : c'est un identifiant technique généré par le backend pour retrouver une requête dans ses journaux.

Codes métier attendus :

- `FOUND` : données trouvées ;
- `NOT_FOUND` : aucune donnée correspondant à la recherche ;
- `INVALID_INPUT` : donnée absente ou format incorrect ;
- `INACTIVE_ACCOUNT` : compte trouvé mais inactif ;
- `RESET_ACCEPTED` : demande de réinitialisation acceptée ;
- `UNAUTHORIZED` : appel non autorisé ;
- `TOO_MANY_REQUESTS` : limite de débit atteinte (ex. réinitialisation déjà demandée récemment) ;
- `TEMPORARY_ERROR` : erreur technique temporaire.

Le backend peut utiliser d'autres libellés, mais il doit fournir la table d'équivalence avant l'intégration.

---

## 1. Vérification d'un agent E-Carrière

### Requête envoyée par le chatbot

```json
{
  "cni": "1234567890123",
  "matricule": "123456A"
}
```

Champs obligatoires : `cni`, `matricule`.

### Réponse attendue — succès

```json
{
  "success": true,
  "code": "FOUND",
  "message": "Agent trouvé",
  "data": {
    "agent_id": "123",
    "nom": "DIOP",
    "prenom": "Aminata",
    "nom_complet": "Aminata DIOP",
    "cni": "1234567890123",
    "matricule": "123456A",
    "email": "aminata.diop@exemple.sn",
    "affectation_id": "45",
    "projets": [
      {
        "numero": "PROJ-001",
        "type": "Avancement",
        "etat": "En cours",
        "date": "2026-06-15"
      }
    ]
  },
  "correlation_id": "a1b2c3d4"
}
```

`projets` peut être une liste vide.

### Réponse attendue — agent non trouvé

```json
{
  "success": false,
  "code": "NOT_FOUND",
  "message": "Aucun agent ne correspond aux informations fournies",
  "data": null
}
```

---

## 2. Consultation des actes E-Carrière

### Requête envoyée par le chatbot

```json
{
  "agent_id": "123"
}
```

Champ obligatoire : `agent_id` (obtenu lors de la vérification de l'agent).

### Réponse attendue

```json
{
  "success": true,
  "code": "FOUND",
  "message": "Actes récupérés",
  "data": {
    "actes": [
      {
        "numero": "ACT-2024-001",
        "type": "Titularisation",
        "etat": "Validé",
        "date": "2024-01-10"
      }
    ]
  }
}
```

`actes: []` est une réponse valide lorsqu'aucun acte n'existe.

---

## 3. Consultation des projets E-Carrière

### Requête envoyée par le chatbot

```json
{
  "agent_id": "123"
}
```

Champ obligatoire : `agent_id`.

### Réponse attendue

```json
{
  "success": true,
  "code": "FOUND",
  "message": "Projets récupérés",
  "data": {
    "projets": [
      {
        "numero": "PROJ-001",
        "type": "Avancement",
        "etat": "En cours",
        "date": "2026-06-15"
      }
    ]
  }
}
```

`projets: []` est une réponse valide lorsqu'aucun projet n'existe.

---

## 4. Réinitialisation du mot de passe E-Carrière

Le chatbot appelle ce service seulement après confirmation explicite de l'utilisateur.

### Requête envoyée par le chatbot

```json
{
  "email": "aminata.diop@exemple.sn"
}
```

Champ obligatoire : `email`.

### Réponse attendue

```json
{
  "success": true,
  "code": "RESET_ACCEPTED",
  "message": "La demande de réinitialisation a été prise en compte",
  "data": null
}
```

Le backend déclenche le processus officiel. Il ne renvoie ni lien de réinitialisation ni mot de passe.

---

## 5. Vérification d'un compte PGDE

### Requête envoyée par le chatbot

```json
{
  "cni": "1234567890123"
}
```

Champ obligatoire : `cni`.

### Réponse attendue — succès

```json
{
  "success": true,
  "code": "FOUND",
  "message": "Compte trouvé",
  "data": {
    "user_id": "789",
    "numero_dossier": "789",
    "nom": "NDIAYE",
    "prenom": "Moussa",
    "nom_complet": "Moussa NDIAYE",
    "username": "mndiaye",
    "email": "moussa.ndiaye@exemple.sn",
    "cni": "1234567890123",
    "actif": true
  }
}
```

Si le compte est désactivé, le backend retourne `success: false` et `code: "INACTIVE_ACCOUNT"`.

---

## 6. Réinitialisation du mot de passe PGDE

Le chatbot appelle ce service seulement après confirmation explicite de l'utilisateur.

### Requête envoyée par le chatbot

```json
{
  "cni": "1234567890123",
  "email": "moussa.ndiaye@exemple.sn"
}
```

Champs obligatoires : `cni`, `email`.

### Réponse attendue

```json
{
  "success": true,
  "code": "RESET_ACCEPTED",
  "message": "La demande de réinitialisation a été prise en compte",
  "data": null
}
```

Le backend déclenche le mécanisme officiel et ne renvoie ni mot de passe ni lien de réinitialisation.

---

## Livrables attendus du backend

Avant l'intégration côté chatbot, le développeur backend fournit :

- les URLs et méthodes HTTP retenues ;
- le mécanisme d'authentification et les en-têtes requis ;
- les réponses exactes pour tous les cas ci-dessus ;
- les codes HTTP utilisés ;
- un environnement de test ou des exemples testables.
