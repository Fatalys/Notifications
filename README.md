# Notifications

Ce projet surveille des pages web pour détecter la disponibilité de produits spécifiques (par exemple, de la RAM 32 Go) et envoie des notifications via ntfy.sh lorsqu'un texte indicateur ("Ajouter au panier") est trouvé sur la page.

## Fonctionnalités

- Vérification automatique de plusieurs URLs.
- Utilisation de Playwright pour un rendu JavaScript complet des pages.
- Détection de blocages Cloudflare.
- Envoi de notifications push via ntfy.sh.

## Prérequis

- Python 3.11 ou supérieur
- Playwright pour le rendu des pages web

## Installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/Fatalys/Notifications.git
   cd Notifications
   ```

2. Installez les dépendances Python :
   ```bash
   pip install -r requirements.txt
   ```

3. Installez les navigateurs Playwright :
   ```bash
   playwright install
   ```

## Configuration

Le script utilise les variables d'environnement suivantes :

- `URLS` : Liste d'URLs à vérifier, séparées par des virgules (ex. : `https://example.com/page1,https://example.com/page2`).
- `NTFY_URL` : URL de votre topic ntfy.sh pour les notifications (ex. : `https://ntfy.sh/mon-topic`).

Vous pouvez définir ces variables dans un fichier `.env` ou directement dans votre environnement.

## Utilisation

Exécutez le script principal :
```bash
python check_page.py
```

Le script vérifiera chaque URL, attendra le chargement de la page, et enverra une notification si le texte "Ajouter au panier" est détecté.

## Workflow GitHub Actions

Ce projet inclut un workflow GitHub Actions qui exécute automatiquement la vérification toutes les 5 minutes. Pour l'utiliser :

1. Ajoutez les secrets suivants dans les paramètres de votre dépôt GitHub :
   - `PAGE_URL` : (Note : Le script utilise `URLS`, mais le workflow a `PAGE_URL` – ajustez si nécessaire)
   - `SEARCH_TEXT` : Texte à rechercher (par défaut "Ajouter au panier")
   - `GOOGLE_CHAT_WEBHOOK` : Webhook pour Google Chat (si utilisé, mais le script utilise ntfy.sh)

2. Le workflow se déclenche sur un planning (toutes les 5 minutes) ou manuellement via `workflow_dispatch`.

Note : Assurez-vous que les variables d'environnement correspondent à celles utilisées dans le script (`URLS` et `NTFY_URL`).

## Licence

Ce projet est sous licence MIT.
