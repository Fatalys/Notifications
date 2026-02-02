import os
import requests
from playwright.sync_api import sync_playwright

URLS_ENV = os.getenv("URLS", "")
NOTIFICATION_URL = os.getenv("NTFY_URL")

TEXTE = os.getenv("SEARCH_TEXT")

if not URLS_ENV:
    raise RuntimeError("Variable d'environnement URLS manquante")

if not NOTIFICATION_URL:
    raise RuntimeError("Variable d'environnement NTFY_URL manquante")

if not TEXTE:
    raise RuntimeError("Variable d'environnement SEARCH_TEXT manquante")

URLS = [u.strip() for u in URLS_ENV.split(",") if u.strip()]


def send_notification(message: str, priority="5", title="RAM 32 Go Disponible"):
    headers = {
        "Priority": priority,
        "Tags": "information_source",
        "Title": title,
    }
    r = requests.post(NOTIFICATION_URL, headers=headers, data=message, timeout=15)
    r.raise_for_status()


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    context = browser.new_context(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 800},
        locale="fr-FR",
        timezone_id="Europe/Paris"
    )

    page = context.new_page()

    for url in URLS:
        print(f"\n🔎 Vérification : {url}")

        page.goto(url, timeout=60000, wait_until="domcontentloaded")
        page.wait_for_timeout(4000)

        html = page.content()

        if "Just a moment" in html:
            print("❌ Cloudflare bloque")
            send_notification(f"Cloudflare bloque l'accès à la page :\n{url}", priority="3", title="Blocage Cloudflare")
            continue

        if TEXTE.lower() in html.lower():
            print("✅ Texte trouvé")
            send_notification(f"✅ Disponible :\n{url}")
        else:
            print("❌ Texte non trouvé")

    browser.close()