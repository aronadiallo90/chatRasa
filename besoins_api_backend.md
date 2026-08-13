# Besoins fonctionnels d'intégration Backend — Chatbot Amath

## Objet

Le chatbot ne doit plus se connecter directement aux bases SQL Server (E-Carrière) ni MySQL (PGDE). Le backend expose les services nécessaires et reste seul responsable de l'accès aux bases, de la logique métier, de la sécurité et des échanges avec les plateformes.

Ce document décrit **ce que le chatbot doit pouvoir faire**. Le choix des URL, des verbes HTTP, du découpage des endpoints et de l'implémentation appartient au développeur backend.

## Règles communes

- Les échanges entre le chatbot et le backend doivent être authentifiés et chiffrés (HTTPS).
- Le backend ne doit jamais renvoyer de mot de passe, secret technique ni détail de connexion à une base.
- Les données retournées doivent être limitées à celles utiles à la conversation.
- Les dates doivent être renvoyées dans un format stable et documenté (idéalement ISO 8601 : `YYYY-MM-DD` ou `YYYY-MM-DDTHH:mm:ssZ`). Le chatbot se charge de l'affichage `JJ/MM/AAAA`.
- Chaque réponse doit permettre au chatbot de distinguer : succès, ressource inexistante, données de saisie invalides, accès refusé et erreur technique temporaire.
- Prévoir un identifiant de corrélation dans les logs/réponses afin de diagnostiquer une erreur sans exposer de données personnelles.

### Enveloppe de réponse recommandée

Le format reste au choix du backend, mais les exemples ci-dessous utilisent l'enveloppe suivante afin que le chatbot puisse être développé sans ambiguïté :

```json
{
  "success": true,
  "code": "FOUND",
  "message": "Agent trouvé",
  "data": {},
  "correlation_id": "a1b2c3d4"
}
```

En cas d'erreur, `success` vaut `false`. Le champ `data` peut être omis ou être `null`. Les noms des champs peuvent être adaptés par le backend, à condition que le contrat final soit communiqué avant l'intégration du chatbot.

## 1. E-Carrière

### 1.1 Vérifier un agent et son compte

Le chatbot fournit une CNI et un matricule solde afin de vérifier qu'ils correspondent au même agent E-Carrière.

**Données fournies par le chatbot**

- CNI (obligatoire) ;
- matricule solde (obligatoire).

**Résultat attendu en cas de succès**

- identifiant technique de l'agent ;
- nom et prénom officiels ;
- matricule ;
- CNI ;
- email associé, s'il existe ;
- identifiant ou libellé d'affectation, si disponible ;
- indication qu'un compte/agent correspondant a été trouvé ;
- les trois projets les plus récents, ou une liste vide.

Pour chaque projet : numéro, type, état et date. Les projets doivent être triés du plus récent au plus ancien.

**Résultats métier à distinguer**

- aucune correspondance CNI + matricule ;
- CNI ou matricule au format invalide ;
- agent trouvé mais sans projet ;
- erreur technique.

**Exemple de requête attendue**

```json
{
  "cni": "1234567890123",
  "matricule": "123456A"
}
```

**Exemple de réponse attendue — agent trouvé**

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

**Exemple de réponse attendue — non trouvé**

```json
{
  "success": false,
  "code": "NOT_FOUND",
  "message": "Aucun agent ne correspond aux informations fournies",
  "data": null,
  "correlation_id": "a1b2c3d4"
}
```

### 1.2 Consulter les actes administratifs d'un agent

Après vérification de l'agent, le chatbot doit pouvoir demander ses actes administratifs.

Le backend doit accepter l'identifiant technique renvoyé à l'étape précédente ou, si ce choix est retenu par le backend, le couple CNI + matricule. Il doit retourner au maximum les trois actes les plus récents, triés du plus récent au plus ancien.

Pour chaque acte : numéro, type, état et date.

Une absence d'acte est un résultat normal : la réponse doit alors contenir une liste vide, et non une erreur.

**Exemple de requête attendue**

```json
{
  "agent_id": "123"
}
```

**Exemple de réponse attendue**

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
  },
  "correlation_id": "a1b2c3d4"
}
```

### 1.3 Consulter les projets d'un agent

Après vérification de l'agent, le chatbot doit pouvoir redemander les projets de l'agent, avec les mêmes règles de tri et de limite que ci-dessus.

Pour chaque projet : numéro, type, état et date. Une liste vide indique qu'aucun projet n'est disponible.

**Exemple de requête attendue**

```json
{
  "agent_id": "123"
}
```

**Exemple de réponse attendue**

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
  },
  "correlation_id": "a1b2c3d4"
}
```

### 1.4 Déclencher une réinitialisation de mot de passe E-Carrière

Le chatbot demande confirmation à l'utilisateur avant d'appeler ce service. Le backend doit ensuite déclencher le processus officiel de réinitialisation pour l'adresse email validée.

**Donnée fournie** : email associé au compte (obligatoire).

**Résultat attendu** : confirmation que la demande a été prise en compte, ou motif fonctionnel exploitable par le chatbot (email introuvable, compte inéligible, demande refusée, erreur temporaire). Pour des raisons de sécurité, la réponse ne doit pas révéler inutilement si une adresse appartient à un compte ; le comportement final sera aligné avec la politique de sécurité de la plateforme.

**Exemple de requête attendue**

```json
{
  "email": "aminata.diop@exemple.sn"
}
```

**Exemple de réponse attendue**

```json
{
  "success": true,
  "code": "RESET_ACCEPTED",
  "message": "La demande de réinitialisation a été prise en compte",
  "data": null,
  "correlation_id": "a1b2c3d4"
}
```

## 2. PGDE

### 2.1 Vérifier un compte utilisateur par CNI

Le chatbot fournit une CNI afin de retrouver le compte PGDE correspondant.

**Donnée fournie** : CNI (obligatoire).

**Résultat attendu en cas de succès**

- identifiant technique ou numéro de dossier ;
- nom et prénom officiels ;
- nom d'utilisateur ;
- email associé ;
- CNI ;
- statut d'activation du compte (`actif` / `inactif` ou équivalent).

**Résultats métier à distinguer**

- aucun compte correspondant ;
- compte trouvé mais inactif/désactivé ;
- CNI invalide ;
- erreur technique.

**Exemple de requête attendue**

```json
{
  "cni": "1234567890123"
}
```

**Exemple de réponse attendue — compte trouvé**

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
  },
  "correlation_id": "a1b2c3d4"
}
```

### 2.2 Déclencher une réinitialisation de mot de passe PGDE

Après confirmation explicite de l'utilisateur, le chatbot doit pouvoir demander l'envoi du mécanisme officiel de réinitialisation de mot de passe PGDE.

**Données fournies**

- CNI ou identifiant utilisateur ;
- email associé au compte.

**Résultat attendu** : confirmation de prise en compte de la demande ou retour d'un état fonctionnel (données incohérentes, compte inactif, demande impossible, erreur temporaire). Le mot de passe et le lien de réinitialisation ne transitent jamais par le chatbot.

**Exemple de requête attendue**

```json
{
  "cni": "1234567890123",
  "email": "moussa.ndiaye@exemple.sn"
}
```

**Exemple de réponse attendue**

```json
{
  "success": true,
  "code": "RESET_ACCEPTED",
  "message": "La demande de réinitialisation a été prise en compte",
  "data": null,
  "correlation_id": "a1b2c3d4"
}
```

## 3. Contrat de données à convenir avec le backend

Le développeur backend choisit le format exact, mais le contrat doit être stable et fournir au minimum :

- un indicateur de résultat ;
- un code métier lisible par le chatbot ;
- un message technique sûr, destiné aux logs ;
- les données utiles lorsque l'opération réussit ;
- un identifiant de corrélation.

Exemples de codes métier possibles : `FOUND`, `NOT_FOUND`, `INVALID_INPUT`, `INACTIVE_ACCOUNT`, `RESET_ACCEPTED`, `UNAUTHORIZED`, `TEMPORARY_ERROR`. Ces libellés sont des exemples, pas une contrainte de nommage.

## 4. Critères d'acceptation

- Aucun composant du chatbot ne possède d'identifiant SQL Server/MySQL ni n'ouvre de connexion directe à une base.
- Pour chaque besoin ci-dessus, le chatbot peut afficher un message approprié pour le succès, l'absence de résultat, une saisie invalide et une panne temporaire.
- Les opérations de consultation respectent les droits d'accès définis par les plateformes.
- Les opérations de réinitialisation sont journalisées, protégées contre les abus et n'exposent aucune donnée sensible.
- La documentation d'intégration fournie par le backend précise l'authentification, les champs requis, les formats, les codes métier, les limites éventuelles et des exemples de réponses.
