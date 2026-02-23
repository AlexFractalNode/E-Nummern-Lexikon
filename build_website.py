import json
import os
import shutil
import re
from datetime import datetime

# --- KONFIGURATION ---
OUTPUT_DIR = 'site_output'
DATA_FILE = 'generated_additives.json'
SITE_NAME = "E-Check Datenbank 📘"
BASE_URL = "https://alexfractalnode.github.io/E-Nummern-Lexikon/" 

# VERLINKUNG ZUR APP (Die Brücke!)
APP_URL = "https://alexfractalnode.github.io/e-check-app/" 
APP_NAME = "E-Check App"

# IMPRESSUM & DATENSCHUTZ KONFIGURATION
IMPRESSUM_NAME = ""
IMPRESSUM_ADRESSE = ""
IMPRESSUM_EMAIL = ""
# Optional: Telefonnummer, falls gewünscht (sonst leer lassen)
IMPRESSUM_TEL = "" 

# MONETARISIERUNG & AFFILIATE
AMAZON_PARTNER_TAG = "dein-tag-21" 
SHOW_ADS = True 

AFFILIATE_MAPPINGS = {
    "süßstoff": "erythrit+bio", "süßungsmittel": "xylit+birkenzucker", "aspartam": "stevia+tropfen+bio",
    "zucker": "kokosblütenzucker", "farbstoff": "natürliche+lebensmittelfarbe", "färben": "färbende+lebensmittel",
    "karmin": "vegane+lebensmittelfarbe", "azo": "natürliche+backzutaten", "geschmacksverstärker": "gewürze+ohne+geschmacksverstärker",
    "glutamat": "gemüsebrühe+hefeextraktfrei", "hefe": "liebstöckel+bio", "konservierungsstoff": "einmachgläser+weck",
    "konservierung": "fermentierset", "nitrit": "rauchsalz+bio", "pökelsalz": "meersalz+unraffiniert",
    "verdickungsmittel": "guarkernmehl+bio", "geliermittel": "agar+agar+bio", "emulgator": "sonnenblumenlecithin+bio",
    "überzugsmittel": "bienenwachstücher", "wachs": "bienenwachs+pastillen", "vaseline": "bio+kokosöl",
    "paraffin": "bienenwachstücher", "säuerungsmittel": "apfelessig+naturtrüb",
}

# --- CSS DESIGN (Mit App-Brücke) ---
css_styles = f"""
<style>
    :root {{ 
        --primary: #10b981; --primary-dark: #059669;
        --bg: #f9fafb; --text: #1f2937; --card-bg: #ffffff; --border: #e5e7eb;
        --app-color: #3b82f6;
    }}
    body {{ font-family: 'Inter', system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }}
    
    /* NAV */
    nav {{ background: white; border-bottom: 1px solid var(--border); padding: 1rem 0; position: sticky; top: 0; z-index: 50; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }}
    .nav-container {{ max-width: 1000px; margin: 0 auto; padding: 0 1.5rem; display: flex; justify-content: space-between; align-items: center; }}
    .logo {{ font-weight: 800; font-size: 1.25rem; color: var(--primary-dark); text-decoration: none; }}
    .nav-links {{ display: flex; align-items: center; }}
    .nav-links a {{ color: #6b7280; text-decoration: none; font-size: 0.9rem; font-weight: 500; margin-left: 1.5rem; }}
    
    /* APP BUTTON IN NAV */
    .nav-app-btn {{ 
        background: var(--app-color); color: white !important; padding: 8px 16px; border-radius: 99px; 
        transition: transform 0.2s; display: inline-flex; align-items: center; gap: 6px;
    }}
    .nav-app-btn:hover {{ transform: scale(1.05); box-shadow: 0 4px 10px rgba(59, 130, 246, 0.3); }}

    /* FLOATING ACTION BUTTON (Mobile Only) */
    .fab-app {{
        position: fixed; bottom: 20px; right: 20px; z-index: 100;
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white; padding: 12px 20px; border-radius: 50px;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
        font-weight: bold; text-decoration: none; display: flex; align-items: center; gap: 8px;
        transition: transform 0.2s; font-size: 0.95rem;
    }}
    .fab-app:hover {{ transform: scale(1.05); }}
    @media(min-width: 800px) {{ .fab-app {{ display: none; }} }} /* PC braucht keinen FAB */

    /* LAYOUT */
    .container {{ max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem; width: 100%; box-sizing: border-box; flex: 1; }}
    .hero {{ text-align: center; padding: 4rem 1rem 3rem 1rem; background: white; border-bottom: 1px solid var(--border); }}
    .hero h1 {{ font-size: 2.5rem; margin-bottom: 0.5rem; color: #111827; }}
    .search-box {{ width: 100%; max-width: 500px; padding: 16px 24px; border: 2px solid #e5e7eb; border-radius: 100px; font-size: 1.1rem; outline: none; margin: 2rem auto 0 auto; display:block; }}
    .search-box:focus {{ border-color: var(--primary); }}

    /* GRID & CARDS */
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 2rem; }}
    .card {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; text-decoration: none; color: inherit; transition: all 0.2s; display: flex; flex-direction: column; height: 100%; }}
    .card:hover {{ transform: translateY(-3px); box-shadow: 0 10px 20px -5px rgba(0,0,0,0.1); border-color: var(--primary); }}
    .card-header {{ display: flex; justify-content: space-between; margin-bottom: 0.5rem; }}
    .e-code {{ font-size: 0.85rem; font-weight: 700; color: #9ca3af; text-transform: uppercase; }}
    .card-title {{ font-size: 1.1rem; font-weight: 700; color: #111827; margin: 0.2rem 0 0.5rem 0; }}
    .card-intro {{ font-size: 0.9rem; color: #6b7280; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }}

    /* BADGES */
    .badge {{ display: inline-flex; align-items: center; padding: 2px 10px; border-radius: 99px; font-size: 0.75rem; font-weight: 700; }}
    .bg-green {{ background-color: #d1fae5; color: #065f46; }}
    .bg-orange {{ background-color: #ffedd5; color: #9a3412; }}
    .bg-red {{ background-color: #fee2e2; color: #991b1b; }}
    
    /* DETAIL PAGE */
    .detail-header {{ background: white; border-bottom: 1px solid var(--border); padding: 3rem 0; text-align: center; }}
    .detail-title {{ font-size: 2.5rem; font-weight: 800; color: #111827; margin: 0.5rem 0; }}
    .section-card {{ background: white; border-radius: 16px; border: 1px solid var(--border); padding: 2rem; margin-bottom: 2rem; }}
    .section-title {{ font-size: 1.25rem; font-weight: 700; color: #111827; margin-bottom: 1rem; }}
    .info-list li {{ padding: 0.75rem 0; border-bottom: 1px solid #f3f4f6; display: flex; justify-content: space-between; }}
    .info-list li:last-child {{ border-bottom: none; }}
    
    /* AFFILIATE BOX */
    .affiliate-box {{ background: linear-gradient(135deg, #fffbeb 0%, #fff7ed 100%); border: 1px solid #fed7aa; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; display: flex; align-items: center; gap: 1.5rem; }}
    .affiliate-icon {{ font-size: 2rem; background: white; width: 60px; height: 60px; display: flex; justify-content: center; align-items: center; border-radius: 50%; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
    .affiliate-btn {{ background: #f97316; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 0.9rem; display: inline-block; margin-top: 0.8rem; }}
    
    /* APP PROMO BOX */
    .app-promo {{ background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 12px; padding: 1.5rem; text-align: center; margin-top: 3rem; }}
    .app-promo h3 {{ color: #1e40af; margin-top: 0; }}
    
    /* LEGAL PAGES */
    .legal-content h1 {{ color: var(--primary-dark); border-bottom: 2px solid var(--border); padding-bottom: 1rem; margin-bottom: 2rem; }}
    .legal-content h2 {{ margin-top: 2rem; color: #374151; }}
    .legal-content h3 {{ margin-top: 1.5rem; color: #4b5563; font-size: 1.1rem; }}
    .legal-content p, .legal-content li {{ color: #6b7280; margin-bottom: 1rem; }}
    
    footer {{ background: white; border-top: 1px solid var(--border); padding: 2rem 0; text-align: center; color: #9ca3af; margin-top: auto; }}
    footer a {{ color: #6b7280; text-decoration: none; margin: 0 10px; font-size: 0.9rem; }}
    footer a:hover {{ color: var(--primary); text-decoration: underline; }}
</style>
"""

# --- HELPER FUNCTIONS ---
def get_risk_class(rating):
    r = str(rating).lower()
    if 'unbedenklich' in r or 'safe' in r: return 'bg-green'
    if 'vorsicht' in r or 'bedenklich' in r: return 'bg-orange'
    return 'bg-red'

def clean_slug(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def get_schema_markup(item):
    schema = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": f"Ist {item['name']} gesund?",
        "description": item.get('meta_description', ''),
        "author": {"@type": "Organization", "name": SITE_NAME},
        "publisher": {"@type": "Organization", "name": SITE_NAME, "logo": {"@type": "ImageObject", "url": f"{BASE_URL}/logo.png"}}
    }
    return json.dumps(schema)

def get_amazon_query(item):
    full_text = (str(item.get('name', '')) + " " + str(item.get('usage', '')) + " " + str(item.get('intro_hook', ''))).lower()
    for keyword, query in AFFILIATE_MAPPINGS.items():
        if keyword in full_text: return query
    return "bio+lebensmittel+ohne+zusatzstoffe"

def get_affiliate_html(item):
    if not SHOW_ADS: return ""
    rating = item.get('health_check', {}).get('rating', 'Unbekannt')
    if get_risk_class(rating) in ['bg-orange', 'bg-red']:
        query = get_amazon_query(item)
        link = f"https://www.amazon.de/s?k={query}&tag={AMAZON_PARTNER_TAG}"
        return f"""
        <div class="affiliate-box">
            <div class="affiliate-icon">🌿</div>
            <div>
                <h4 style="margin:0 0 5px 0; color:#9a3412;">Gesunde Alternative?</h4>
                <p style="margin:0; font-size:0.95rem; color:#4b5563;">Vermeide Chemie. Hier gibt es natürliche Alternativen.</p>
                <a href="{link}" target="_blank" rel="nofollow" class="affiliate-btn">Bio-Alternativen bei Amazon ↗</a>
            </div>
        </div>
        """
    return ""

def build_nav():
    return f"""
    <nav>
        <div class="nav-container">
            <a href="index.html" class="logo">🧬 {SITE_NAME}</a>
            <div class="nav-links">
                <a href="index.html">Lexikon</a>
                <a href="{APP_URL}" target="_blank" class="nav-app-btn">📱 App laden</a>
            </div>
        </div>
    </nav>
    """

def build_footer():
    return f"""
    <footer>
        <p>&copy; {datetime.now().year} {SITE_NAME}</p>
        <div style="margin-top: 10px;">
            <a href="impressum.html">Impressum</a> • 
            <a href="datenschutz.html">Datenschutzerklärung</a> • 
            <a href="{APP_URL}" target="_blank">Zur App</a>
        </div>
    </footer>
    """

def build_impressum():
    """Generiert die Impressum-Seite"""
    html = f"""
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Impressum | {SITE_NAME}</title>
        {css_styles}
    </head>
    <body>
        {build_nav()}
        <main class="container legal-content">
            <div class="section-card">
                <h1>Impressum</h1>
                <p>Angaben gemäß § 5 TMG</p>
                
                <h2>Betreiber der Website</h2>
                <p>
                    <strong>{IMPRESSUM_NAME}</strong><br>
                    {IMPRESSUM_ADRESSE}
                </p>

                <h2>Kontakt</h2>
                <p>
                    E-Mail: <a href="mailto:{IMPRESSUM_EMAIL}">{IMPRESSUM_EMAIL}</a>
                    {f'<br>Telefon: {IMPRESSUM_TEL}' if IMPRESSUM_TEL else ''}
                </p>

                <h2>Verantwortlich für den Inhalt</h2>
                <p>
                    Verantwortlich nach § 55 Abs. 2 RStV:<br>
                    {IMPRESSUM_NAME}<br>
                    {IMPRESSUM_ADRESSE}
                </p>

                <h2>Haftungsausschluss</h2>
                <h3>Haftung für Inhalte</h3>
                <p>Die Inhalte unserer Seiten wurden mit größter Sorgfalt erstellt. Für die Richtigkeit, Vollständigkeit und Aktualität der Inhalte können wir jedoch keine Gewähr übernehmen.</p>

                <h3>Haftung für Links</h3>
                <p>Unser Angebot enthält Links zu externen Webseiten Dritter, auf deren Inhalte wir keinen Einfluss haben. Deshalb können wir für diese fremden Inhalte auch keine Gewähr übernehmen.</p>
            </div>
        </main>
        {build_footer()}
    </body>
    </html>
    """
    with open(os.path.join(OUTPUT_DIR, "impressum.html"), "w", encoding="utf-8") as f: f.write(html)

def build_datenschutz():
    """Generiert die Datenschutz-Seite"""
    html = f"""
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Datenschutzerklärung | {SITE_NAME}</title>
        {css_styles}
    </head>
    <body>
        {build_nav()}
        <main class="container legal-content">
            <div class="section-card">
                <h1>Datenschutzerklärung</h1>
                
                <h2>1. Datenschutz auf einen Blick</h2>
                <h3>Allgemeine Hinweise</h3>
                <p>Die folgenden Hinweise geben einen einfachen Überblick darüber, was mit Ihren personenbezogenen Daten passiert, wenn Sie diese Website besuchen.</p>

                <h2>2. Hosting (GitHub Pages)</h2>
                <p>Wir hosten unsere Website bei <strong>GitHub Inc.</strong> (88 Colin P Kelly Jr St, San Francisco, CA 94107, USA).<br>
                GitHub erfasst Logfiles (IP-Adresse, Browser, etc.) zur Sicherheit und Stabilität. Weitere Infos: <a href="https://docs.github.com/en/site-policy/privacy-policies/github-privacy-statement" target="_blank">GitHub Privacy Statement</a>.</p>

                <h2>3. Cookies & Analyse</h2>
                <p>Diese Website verwendet keine Tracking-Cookies und keine Analyse-Tools (wie Google Analytics). Es werden lediglich technisch notwendige Daten durch den Hoster (GitHub) verarbeitet.</p>

                <h2>4. Affiliate Links (Amazon)</h2>
                <p>Wir nehmen am Amazon Partnerprogramm teil. Wenn Sie auf einen Amazon-Link klicken, gelangt Amazon an die Information, dass Sie von unserer Seite kommen (Referrer). Es werden keine persönlichen Daten von uns an Amazon übermittelt.</p>

                <h2>5. Ihre Rechte</h2>
                <p>Sie haben jederzeit das Recht auf Auskunft, Berichtigung oder Löschung Ihrer Daten. Wenden Sie sich dazu an die im Impressum angegebene Adresse.</p>
            </div>
        </main>
        {build_footer()}
    </body>
    </html>
    """
    with open(os.path.join(OUTPUT_DIR, "datenschutz.html"), "w", encoding="utf-8") as f: f.write(html)


# --- BUILD PROCESS ---
def build():
    if os.path.exists(OUTPUT_DIR): shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f: additives = json.load(f)
        print(f"✅ {len(additives)} Einträge geladen.")
    except Exception as e:
        print(f"❌ Fehler: {e}"); return

    sitemap_urls = []
    
    # 1. DETAIL SEITEN
    for item in additives:
        slug = clean_slug(f"{item.get('e_number', '')}-{item.get('name', '')}")
        filename = f"{slug}.html"
        rating = item.get('health_check', {}).get('rating', 'Unbekannt')
        rating_class = get_risk_class(rating)
        
        html = f"""
        <!DOCTYPE html>
        <html lang="de">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{item.get('seo_title', item.get('name'))} | E-Check</title>
            <meta name="description" content="{item.get('meta_description', '')}">
            <script type="application/ld+json">{get_schema_markup(item)}</script>
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
                {get_affiliate_html(item)}
                
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
                            <li><span>Vegan?</span> <strong>{"Ja 🌱" if item.get('dietary_info', {}).get('is_vegan') else "Nein 🥩"}</strong></li>
                            <li><span>Glutenfrei?</span> <strong>{"Ja 🍞" if item.get('dietary_info', {}).get('is_gluten_free') else "Nein 🌾"}</strong></li>
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
                    
                    <div class="app-promo">
                        <h3>⚡ Schneller checken?</h3>
                        <p>Stehst du gerade im Supermarkt? Scanne den Barcode direkt mit unserer App.</p>
                        <a href="{APP_URL}" target="_blank" class="nav-app-btn" style="display:inline-flex;">📲 Scanner App öffnen</a>
                    </div>
                </div>

                <div style="text-align:center; margin-top:2rem;">
                    <a href="index.html" style="color:var(--primary); font-weight:600; text-decoration:none;">← Zurück zur Übersicht</a>
                </div>
            </main>
            
            <a href="{APP_URL}" target="_blank" class="fab-app">
                <span style="font-size:1.2rem;">📷</span> Jetzt scannen
            </a>
            
            {build_footer()}
        </body>
        </html>
        """
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f: f.write(html)
        sitemap_urls.append(f"{BASE_URL}/{filename}")

    # 2. INDEX
    cards_html = ""
    for item in additives:
        slug = clean_slug(f"{item.get('e_number', '')}-{item.get('name', '')}")
        rating = item.get('health_check', {}).get('rating', '')
        cards_html += f"""<a href="{slug}.html" class="card filter-item"><div class="card-header"><span class="e-code">{item.get('e_number')}</span><span class="badge {get_risk_class(rating)}">{rating}</span></div><h3 class="card-title">{item.get('name')}</h3><p class="card-intro">{item.get('intro_hook')}</p></a>"""
    
    index_html = f"""<!DOCTYPE html><html lang="de"><head><title>{SITE_NAME}</title><meta name="viewport" content="width=device-width, initial-scale=1">{css_styles}<script>function filterList() {{ var input = document.getElementById("search"); var filter = input.value.toUpperCase(); var cards = document.getElementsByClassName("filter-item"); for (var i = 0; i < cards.length; i++) {{ var txt = cards[i].innerText; if (txt.toUpperCase().indexOf(filter) > -1) {{ cards[i].style.display = "flex"; }} else {{ cards[i].style.display = "none"; }} }} }}</script></head><body>{build_nav()}<div class="hero"><h1>Was steckt in deinem Essen?</h1><p>Die große Datenbank. Oder nutze direkt unsere <a href="{APP_URL}" style="color:var(--app-color);">Scanner App</a>.</p><input type="text" id="search" onkeyup="filterList()" class="search-box" placeholder="🔍 E-Nummer suchen..."></div><main class="container"><div class="grid">{cards_html}</div></main><a href="{APP_URL}" target="_blank" class="fab-app"><span>📷</span> Jetzt scannen</a>{build_footer()}</body></html>"""
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f: f.write(index_html)
    
    # 3. LEGAL PAGES (Funktionen aufrufen)
    build_impressum()
    build_datenschutz()
    
    # 4. SITEMAP
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join([f'  <url><loc>{u}</loc></url>\n' for u in sitemap_urls]) + '</urlset>'
    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f: f.write(sitemap)

    print(f"✅ Webseite V3.0 mit App-Brücke & Rechtstexten generiert!")

if __name__ == "__main__":
    build()

