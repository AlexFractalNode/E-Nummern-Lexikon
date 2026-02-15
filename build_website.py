import json
import os
import shutil
import re
from datetime import datetime

# --- KONFIGURATION ---
OUTPUT_DIR = 'site_output'
DATA_FILE = 'generated_additives.json'
SITE_NAME = "E-Check Datenbank 📘"
BASE_URL = "https://[AlexFractalNode].github.io/[E-Nummern-Lexikon]"

# IMPRESSUM & DATENSCHUTZ (Deine Daten hier eintragen!)
IMPRESSUM_NAME = "Alexander Heinze"
IMPRESSUM_ADRESSE = "Am Fuchsgraben 28, 08056 Zwickau"
IMPRESSUM_EMAIL = "alexander.heinze.01@gmail.com"

# --- CSS DESIGN (Modern & Professional) ---
css_styles = """
<style>
    :root { 
        --primary: #10b981; /* Modernes Grün */
        --primary-dark: #059669;
        --bg: #f3f4f6; 
        --text: #1f2937; 
        --card-bg: #ffffff;
        --border: #e5e7eb;
    }
    body { font-family: 'Inter', system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }
    
    /* Navigation */
    nav { background: white; border-bottom: 1px solid var(--border); padding: 1rem 0; position: sticky; top: 0; z-index: 50; }
    .nav-container { max-width: 1000px; margin: 0 auto; padding: 0 1.5rem; display: flex; justify-content: space-between; align-items: center; }
    .logo { font-weight: 800; font-size: 1.25rem; color: var(--primary-dark); text-decoration: none; display: flex; align-items: center; gap: 8px; }
    .nav-links a { color: #6b7280; text-decoration: none; font-size: 0.9rem; font-weight: 500; margin-left: 1.5rem; transition: color 0.2s; }
    .nav-links a:hover { color: var(--primary); }

    /* Layout */
    .container { max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem; width: 100%; box-sizing: border-box; flex: 1; }
    
    /* Hero Section (Startseite) */
    .hero { text-align: center; padding: 3rem 1rem; }
    .hero h1 { font-size: 2.5rem; margin-bottom: 0.5rem; letter-spacing: -0.025em; color: #111827; }
    .hero p { color: #6b7280; font-size: 1.1rem; max-width: 600px; margin: 0 auto 2rem auto; }
    
    /* Search Bar */
    .search-box { width: 100%; max-width: 500px; padding: 14px 20px; border: 1px solid #d1d5db; border-radius: 12px; font-size: 1rem; outline: none; transition: border-color 0.2s; display: block; margin: 0 auto; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
    .search-box:focus { border-color: var(--primary); ring: 2px solid var(--primary); }

    /* Grid (Cards) */
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 2rem; }
    
    /* Cards */
    .card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; text-decoration: none; color: inherit; transition: all 0.2s; display: flex; flex-direction: column; height: 100%; position: relative; }
    .card:hover { transform: translateY(-3px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); border-color: var(--primary); }
    
    .card-header { display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem; }
    .e-code { font-size: 0.85rem; font-weight: 700; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; }
    .card-title { font-size: 1.1rem; font-weight: 700; color: #111827; margin: 0.2rem 0 0.5rem 0; }
    .card-intro { font-size: 0.9rem; color: #6b7280; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }

    /* Badges */
    .badge { display: inline-flex; align-items: center; padding: 2px 10px; border-radius: 99px; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.025em; }
    .bg-green { background-color: #d1fae5; color: #065f46; }
    .bg-orange { background-color: #ffedd5; color: #9a3412; }
    .bg-red { background-color: #fee2e2; color: #991b1b; }
    
    /* Detail Page */
    .detail-header { background: white; border-bottom: 1px solid var(--border); padding: 3rem 0; text-align: center; }
    .detail-title { font-size: 2.5rem; font-weight: 800; color: #111827; margin: 0.5rem 0; }
    .detail-subtitle { color: #6b7280; font-size: 1.1rem; }
    
    .section-card { background: white; border-radius: 12px; border: 1px solid var(--border); padding: 2rem; margin-bottom: 2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .section-title { font-size: 1.25rem; font-weight: 700; color: #111827; margin-bottom: 1rem; border-bottom: 2px solid #f3f4f6; padding-bottom: 0.5rem; display: flex; align-items: center; gap: 8px; }
    
    .info-list { list-style: none; padding: 0; margin: 0; }
    .info-list li { padding: 0.75rem 0; border-bottom: 1px solid #f3f4f6; display: flex; justify-content: space-between; }
    .info-list li:last-child { border-bottom: none; }
    .info-label { font-weight: 500; color: #6b7280; }
    .info-value { font-weight: 600; color: #111827; }

    /* Footer */
    footer { background: white; border-top: 1px solid var(--border); padding: 2rem 0; text-align: center; color: #9ca3af; font-size: 0.9rem; margin-top: auto; }
    footer a { color: #6b7280; text-decoration: none; margin: 0 10px; }
    footer a:hover { color: var(--primary); }
</style>
"""

# --- HELPER FUNCTIONS ---
def get_risk_class(rating):
    r = str(rating).lower()
    if 'unbedenklich' in r or 'safe' in r: return 'bg-green'
    if 'vorsicht' in r or 'bedenklich' in r or 'caution' in r: return 'bg-orange'
    return 'bg-red' # Default für "Gefährlich" oder unbekannt

def clean_slug(text):
    # Erstellt saubere URL: "E100 Kurkumin" -> "e100-kurkumin"
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

# --- TEMPLATES ---
def build_nav(active_page=""):
    return f"""
    <nav>
        <div class="nav-container">
            <a href="index.html" class="logo">🧬 {SITE_NAME}</a>
            <div class="nav-links">
                <a href="index.html">Übersicht</a>
                <a href="impressum.html">Rechtliches</a>
            </div>
        </div>
    </nav>
    """

# --- MAIN BUILD PROCESS ---
def build():
    # 1. Output Ordner vorbereiten
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # 2. Daten laden
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            additives = json.load(f)
        print(f"✅ {len(additives)} Einträge geladen.")
    except Exception as e:
        print(f"❌ Fehler beim Laden von {DATA_FILE}: {e}")
        return

    # 3. Detailseiten generieren
    sitemap_urls = []
    
    for item in additives:
        # Daten vorbereiten
        slug = clean_slug(f"{item.get('e_number', '')}-{item.get('name', '')}")
        filename = f"{slug}.html"
        
        rating = item.get('health_check', {}).get('rating', 'Unbekannt')
        rating_class = get_risk_class(rating)
        
        diet = item.get('dietary_info', {})
        is_vegan = "Ja 🌱" if diet.get('is_vegan') else "Nein 🥩"
        is_gluten = "Ja 🍞" if diet.get('is_gluten_free') else "Nein 🌾" # Achtung Logik: Ist glutenfrei? Ja.

        # HTML Template füllen
        html = f"""
        <!DOCTYPE html>
        <html lang="de">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{item.get('seo_title', item.get('name'))} | {SITE_NAME}</title>
            <meta name="description" content="{item.get('meta_description', '')}">
            {css_styles}
        </head>
        <body>
            {build_nav()}
            
            <header class="detail-header">
                <div class="nav-container" style="flex-direction:column;">
                    <span class="e-code">{item.get('e_number')}</span>
                    <h1 class="detail-title">{item.get('name')}</h1>
                    <span class="badge {rating_class}" style="padding: 6px 16px; font-size: 1rem;">{rating}</span>
                </div>
            </header>
            
            <main class="container">
                <div class="section-card">
                    <h2 class="section-title">💡 Überblick</h2>
                    <p style="font-size: 1.1rem; color: #4b5563;">{item.get('intro_hook')}</p>
                </div>

                <div class="grid" style="margin-top:0; margin-bottom: 2rem;">
                    <div class="section-card" style="margin-bottom:0;">
                        <h3 class="section-title">🏥 Gesundheits-Check</h3>
                        <p>{item.get('health_check', {}).get('details')}</p>
                    </div>
                    <div class="section-card" style="margin-bottom:0;">
                        <h3 class="section-title">🥗 Ernährung</h3>
                        <ul class="info-list">
                            <li><span class="info-label">Vegan?</span> <span class="info-value">{is_vegan}</span></li>
                            <li><span class="info-label">Glutenfrei?</span> <span class="info-value">{is_gluten}</span></li>
                            <li><span class="info-label">Herkunft</span> <span class="info-value" style="text-align:right; font-size:0.9rem;">{diet.get('origin_explanation')}</span></li>
                        </ul>
                    </div>
                </div>

                <div class="section-card">
                    <h3 class="section-title">🏭 Verwendung</h3>
                    <p>{item.get('usage')}</p>
                </div>

                <div class="section-card" style="border-left: 4px solid var(--primary);">
                    <h3 class="section-title">🏁 Fazit</h3>
                    <p>{item.get('conclusion')}</p>
                </div>

                <div style="text-align:center; margin-top:2rem;">
                    <a href="index.html" style="color:var(--primary); font-weight:600; text-decoration:none;">← Zurück zur Übersicht</a>
                </div>
            </main>
            
            <footer>
                <p>&copy; {datetime.now().year} {SITE_NAME}</p>
                <a href="impressum.html">Impressum</a> • <a href="datenschutz.html">Datenschutz</a>
            </footer>
        </body>
        </html>
        """
        
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(html)
        sitemap_urls.append(f"{BASE_URL}/{filename}")

    # 4. Index Seite generieren
    print("🔨 Generiere Index...")
    cards_html = ""
    for item in additives:
        slug = clean_slug(f"{item.get('e_number', '')}-{item.get('name', '')}")
        rating = item.get('health_check', {}).get('rating', '')
        rating_class = get_risk_class(rating)
        
        cards_html += f"""
        <a href="{slug}.html" class="card filter-item">
            <div class="card-header">
                <span class="e-code">{item.get('e_number')}</span>
                <span class="badge {rating_class}">{rating}</span>
            </div>
            <h3 class="card-title">{item.get('name')}</h3>
            <p class="card-intro">{item.get('intro_hook')}</p>
        </a>
        """

    index_html = f"""
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <title>{SITE_NAME} - Alle Zusatzstoffe im Check</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="description" content="Ist das gesund? Die große Datenbank für Lebensmittel-Zusatzstoffe, E-Nummern und Inhaltsstoffe.">
        {css_styles}
        <script>
        function filterList() {{
            var input = document.getElementById("search");
            var filter = input.value.toUpperCase();
            var cards = document.getElementsByClassName("filter-item");
            
            for (var i = 0; i < cards.length; i++) {{
                var txt = cards[i].innerText;
                if (txt.toUpperCase().indexOf(filter) > -1) {{
                    cards[i].style.display = "flex";
                }} else {{
                    cards[i].style.display = "none";
                }}
            }}
        }}
        </script>
    </head>
    <body>
        {build_nav()}
        
        <div class="hero">
            <h1>Was steckt wirklich in deinem Essen?</h1>
            <p>Die transparente Enzyklopädie für Zusatzstoffe. KI-analysiert & verständlich.</p>
            <input type="text" id="search" onkeyup="filterList()" class="search-box" placeholder="🔍 Suche nach E120, Vaseline, Farbstoff...">
        </div>
        
        <main class="container">
            <div class="grid">
                {cards_html}
            </div>
        </main>
        
        <footer>
            <p>&copy; {datetime.now().year} {SITE_NAME}</p>
            <a href="impressum.html">Impressum</a> • <a href="datenschutz.html">Datenschutz</a>
        </footer>
    </body>
    </html>
    """
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    # 5. Rechtstexte generieren (Job-Radar Professional Style)
    impressum_html = f"""
    <!DOCTYPE html>
    <html lang="de">
    <head><title>Impressum | {SITE_NAME}</title><meta name="viewport" content="width=device-width, initial-scale=1">{css_styles}</head>
    <body>
        {build_nav()}
        <main class="container" style="max-width:800px;">
            <div class="section-card">
                <h1 style="margin-bottom:2rem;">Impressum</h1>
                <p>Angaben gemäß § 5 TMG</p>
                <p><strong>{IMPRESSUM_NAME}</strong><br>{IMPRESSUM_ADRESSE}</p>
                <p><strong>Kontakt:</strong><br>E-Mail: {IMPRESSUM_EMAIL}</p>
                <p><strong>Haftungsausschluss:</strong><br>Die Inhalte wurden mit KI-Unterstützung erstellt. Wir übernehmen keine Gewähr für die Richtigkeit, Vollständigkeit und Aktualität der bereitgestellten Informationen, insbesondere zu gesundheitlichen Aspekten. Diese Seite ersetzt keine ärztliche Beratung.</p>
            </div>
            <a href="index.html" style="color:var(--primary);">← Zurück zur Startseite</a>
        </main>
        <footer><p>&copy; {datetime.now().year} {SITE_NAME}</p></footer>
    </body>
    </html>
    """
    
    datenschutz_html = f"""
    <!DOCTYPE html>
    <html lang="de">
    <head><title>Datenschutz | {SITE_NAME}</title><meta name="viewport" content="width=device-width, initial-scale=1">{css_styles}</head>
    <body>
        {build_nav()}
        <main class="container" style="max-width:800px;">
            <div class="section-card">
                <h1 style="margin-bottom:2rem;">Datenschutzerklärung</h1>
                <h2>1. Datenschutz auf einen Blick</h2>
                <p><strong>Allgemeine Hinweise</strong><br>Wir nehmen den Schutz Ihrer persönlichen Daten sehr ernst. Diese Webseite speichert keine persönlichen Daten der Nutzer und verwendet keine Tracking-Cookies.</p>
                <p><strong>Hosting bei GitHub Pages</strong><br>Diese Seite wird bei GitHub Inc. gehostet. GitHub kann technische Log-Daten (IP-Adressen) zur Gewährleistung der Sicherheit und Stabilität des Dienstes erfassen. Weitere Informationen finden Sie in der Datenschutzerklärung von GitHub.</p>
                <h2>2. Cookies & Tracking</h2>
                <p>Wir setzen auf dieser Seite keine Analyse-Tools (wie Google Analytics) und keine Werbe-Tracker ein.</p>
            </div>
            <a href="index.html" style="color:var(--primary);">← Zurück zur Startseite</a>
        </main>
        <footer><p>&copy; {datetime.now().year} {SITE_NAME}</p></footer>
    </body>
    </html>
    """
    
    with open(os.path.join(OUTPUT_DIR, "impressum.html"), "w", encoding="utf-8") as f: f.write(impressum_html)
    with open(os.path.join(OUTPUT_DIR, "datenschutz.html"), "w", encoding="utf-8") as f: f.write(datenschutz_html)

    # 6. Sitemap
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap_urls.append(f"{BASE_URL}/")
    for url in sitemap_urls:
        sitemap_xml += f'  <url><loc>{url}</loc><changefreq>monthly</changefreq></url>\n'
    sitemap_xml += '</urlset>'
    
    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_xml)

    print(f"✅ Fertig! Webseite im Ordner '{OUTPUT_DIR}' erstellt.")

if __name__ == "__main__":
    build()
