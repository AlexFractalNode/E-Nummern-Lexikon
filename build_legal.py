import os

# --- KONFIGURATION ---
# Hier deine echten Daten eintragen (oder später im HTML ändern)
BETREIBER_NAME = "Alexander HHeinze"
ADRESSE_STRASSE = "Am Fuchsgraben 28"
ADRESSE_ORT = "08056 Zwickau"
KONTAKT_EMAIL = "alexander.heinze.01@gmail.com"
KONTAKT_TEL = "-" # Optional

# Design (E-Nummern Grün/Dark)
THEME_COLOR = "#10b981" # Smaragdgrün
BG_COLOR = "#0f172a"
TEXT_COLOR = "#f8fafc"

CSS = f"""
<style>
    :root {{ --bg: {BG_COLOR}; --text: {TEXT_COLOR}; --primary: {THEME_COLOR}; --card: #1e293b; }}
    body {{ font-family: -apple-system, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; margin: 0; padding: 0; }}
    .container {{ max-width: 800px; margin: 0 auto; padding: 2rem 1rem; }}
    h1 {{ color: var(--primary); border-bottom: 2px solid var(--primary); padding-bottom: 1rem; margin-bottom: 2rem; }}
    h2 {{ margin-top: 2rem; color: #fff; }}
    h3 {{ margin-top: 1.5rem; color: #cbd5e1; }}
    p, li {{ color: #94a3b8; margin-bottom: 1rem; }}
    a {{ color: var(--primary); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .card {{ background: var(--card); padding: 2rem; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); }}
    .back-btn {{ display: inline-block; margin-bottom: 2rem; color: var(--text); font-weight: bold; }}
</style>
"""

def build_impressum():
    html = f"""
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Impressum | E-Nummern Lexikon</title>
        {CSS}
    </head>
    <body>
        <div class="container">
            <a href="index.html" class="back-btn">← Zurück zur App</a>
            
            <div class="card">
                <h1>Impressum</h1>
                <p>Angaben gemäß § 5 TMG</p>
                
                <h2>Betreiber der Website</h2>
                <p>
                    <strong>{BETREIBER_NAME}</strong><br>
                    {ADRESSE_STRASSE}<br>
                    {ADRESSE_ORT}
                </p>

                <h2>Kontakt</h2>
                <p>
                    E-Mail: <a href="mailto:{KONTAKT_EMAIL}">{KONTAKT_EMAIL}</a><br>
                    Telefon: {KONTAKT_TEL}
                </p>

                <h2>Verantwortlich für den Inhalt</h2>
                <p>
                    Verantwortlich nach § 55 Abs. 2 RStV:<br>
                    {BETREIBER_NAME}<br>
                    {ADRESSE_STRASSE}<br>
                    {ADRESSE_ORT}
                </p>

                <h2>Haftungsausschluss</h2>
                <h3>Haftung für Inhalte</h3>
                <p>Die Inhalte unserer Seiten wurden mit größter Sorgfalt erstellt. Für die Richtigkeit, Vollständigkeit und Aktualität der Inhalte können wir jedoch keine Gewähr übernehmen. Als Diensteanbieter sind wir gemäß § 7 Abs.1 TMG für eigene Inhalte auf diesen Seiten nach den allgemeinen Gesetzen verantwortlich.</p>

                <h3>Haftung für Links</h3>
                <p>Unser Angebot enthält Links zu externen Webseiten Dritter, auf deren Inhalte wir keinen Einfluss haben. Deshalb können wir für diese fremden Inhalte auch keine Gewähr übernehmen. Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber der Seiten verantwortlich.</p>
            </div>
        </div>
    </body>
    </html>
    """
    with open("impressum.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ impressum.html erstellt")

def build_datenschutz():
    html = f"""
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Datenschutzerklärung | E-Nummern Lexikon</title>
        {CSS}
    </head>
    <body>
        <div class="container">
            <a href="index.html" class="back-btn">← Zurück zur App</a>
            
            <div class="card">
                <h1>Datenschutzerklärung</h1>
                
                <h2>1. Datenschutz auf einen Blick</h2>
                <h3>Allgemeine Hinweise</h3>
                <p>Die folgenden Hinweise geben einen einfachen Überblick darüber, was mit Ihren personenbezogenen Daten passiert, wenn Sie diese Website besuchen. Personenbezogene Daten sind alle Daten, mit denen Sie persönlich identifiziert werden können.</p>

                <h2>2. Hosting (GitHub Pages)</h2>
                <p>Wir hosten unsere Website bei <strong>GitHub Inc.</strong> (88 Colin P Kelly Jr St, San Francisco, CA 94107, USA).</p>
                <p>GitHub erfasst beim Besuch der Website Logfiles (z.B. IP-Adresse, Browser, Datum des Zugriffs). Dies ist technisch notwendig, um die Website sicher und stabil bereitzustellen. Weitere Informationen finden Sie in der Datenschutzerklärung von GitHub: <a href="https://docs.github.com/en/site-policy/privacy-policies/github-privacy-statement" target="_blank">GitHub Privacy Statement</a>.</p>

                <h2>3. Datenerfassung in der App</h2>
                <h3>Lokale Speicherung (LocalStorage)</h3>
                <p>Diese App speichert Daten (z.B. Ihren Scan-Verlauf oder Einstellungen) ausschließlich lokal auf Ihrem Endgerät im sogenannten "LocalStorage" Ihres Browsers. Diese Daten werden <strong>nicht</strong> an unsere Server übertragen und sind für uns nicht einsehbar. Sie können diese Daten jederzeit löschen, indem Sie den Browser-Cache leeren.</p>
                
                <h3>Kamera-Zugriff</h3>
                <p>Für die Scan-Funktion benötigt die App Zugriff auf Ihre Kamera. Der Video-Stream wird ausschließlich lokal auf Ihrem Gerät verarbeitet, um Barcodes zu erkennen. Es werden keine Bilder oder Videos an Server übertragen oder gespeichert.</p>

                <h3>Cookies</h3>
                <p>Diese Website verwendet technisch notwendige Mechanismen, setzt aber keine Tracking-Cookies zu Werbezwecken ein.</p>

                <h2>4. Analyse-Tools und Werbung</h2>
                <h3>Amazon Partnerprogramm</h3>
                <p>Wir sind Teilnehmer des Partnerprogramms von Amazon EU, das zur Bereitstellung eines Mediums für Websites konzipiert wurde, mittels dessen durch die Platzierung von Werbeanzeigen und Links zu Amazon.de Werbekostenerstattung verdient werden kann. Amazon setzt Cookies ein, um die Herkunft der Bestellungen nachvollziehen zu können. Dadurch kann Amazon erkennen, dass Sie den Partnerlink auf dieser Website geklickt haben.</p>

                <h2>5. Ihre Rechte</h2>
                <p>Sie haben jederzeit das Recht auf unentgeltliche Auskunft über Ihre gespeicherten personenbezogenen Daten, deren Herkunft und Empfänger und den Zweck der Datenverarbeitung sowie ein Recht auf Berichtigung oder Löschung dieser Daten. Hierzu sowie zu weiteren Fragen zum Thema personenbezogene Daten können Sie sich jederzeit an uns wenden.</p>
                <p>Kontakt: <a href="mailto:{KONTAKT_EMAIL}">{KONTAKT_EMAIL}</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    with open("datenschutz.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ datenschutz.html erstellt")

if __name__ == "__main__":
    build_impressum()
    build_datenschutz()
