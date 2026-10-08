# Widget Amath — ajouter le chatbot sur un site du Ministère

## Intégration : une seule ligne

Coller juste avant `</body>` :

```html
<script src="https://<serveur-chatbot>/widget/amath.js" defer
        data-endpoint="https://<serveur-chatbot>/api/messages"
        data-site="nom-du-site"></script>
```

C'est tout. Une bulle verte « Besoin d'aide ? » apparaît en bas à droite.

> `<serveur-chatbot>` : adresse HTTPS fournie par l'équipe réseau (pas encore disponible).

## Réglages (facultatifs)

| Attribut | Rôle | Exemple |
|---|---|---|
| `data-site` | Nom du site (statistiques) | `ecarriere`, `pgde`, `portail` |
| `data-platform` | Démarre directement sur une plateforme | `E-Carrière`, `PGDE`, `Attestation` |
| `data-z-index` | Si la bulle passe au-dessus d'une fenêtre du site, baisser la valeur (défaut `1040`) | `900` |
| `data-position` | Bulle à gauche | `left` |
| `data-label` | Texte du bouton | `Une question ?` |

Exemple pour le site E-Carrière :

```html
<script src="https://<serveur-chatbot>/widget/amath.js" defer
        data-endpoint="https://<serveur-chatbot>/api/messages"
        data-site="ecarriere" data-platform="E-Carrière"></script>
```

## Ouvrir le chat depuis un bouton du site

```html
<button onclick="AmathChat.open()">Parler à Amath</button>
```

Aussi disponibles : `AmathChat.close()` et `AmathChat.restart()`.

## Bon à savoir

- **Aucune dépendance** : pas de jQuery, Bootstrap ni Font Awesome nécessaires.
- **N'abîme pas le site** : le widget est isolé (Shadow DOM), le CSS du site ne le touche pas et inversement.
- **La conversation suit le visiteur** d'une page à l'autre du même site.
- **Mobile** : plein écran. **Impression** : masqué.
- `data-endpoint` accepte aussi le relais Laravel PGDE (`/api/v1/chatbot/messages`).

## Tester en local

```powershell
# Rasa (5005) et le serveur d'actions doivent tourner (voir le README principal)
cd C:\Users\Arona\Desktop\fp\test\pycharm\pycharm\widget
..\.venv\Scripts\python.exe -m http.server 8002
```

Ouvrir http://127.0.0.1:8002/demo.html — la page imite un site au style agressif
(boutons rouges, Comic Sans) pour vérifier que le widget n'est pas affecté.

Variantes : `demo.html?platform=E-Carrière`, `demo.html?endpoint=relais` (passe par Laravel sur le port 8000).
