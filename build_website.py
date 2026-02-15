import json
import os
import shutil
import re
import urllib.parse
from datetime import datetime

# --- KONFIGURATION ---
OUTPUT_DIR = 'site_output'
DATA_FILE = 'generated_additives.json'
SITE_NAME = "E-Check Datenbank 📘"
BASE_URL = "https://[AlexFractalNode].github.io/[E-Nummern-Lexikon]"

# IMPRESSUM
IMPRESSUM_NAME = "Alexander Heinze"
IMPRESSUM_ADRESSE = "Am Fuchsgraben 28, 08056 Zwickau"
IMPRESSUM_EMAIL = "alexander.heinze.01@gmail.com"

# MONETARISIERUNG
AMAZON_PARTNER_TAG = "dein-tag-21" 
SHOW_ADS = True 

# SMART AFFILIATE MAPPING 🧠
# Hier definieren wir, welches Keyword zu welcher Amazon-Suche führt
AFFILIATE_MAPPINGS = {
    # Süßungsmittel
    "süßstoff": "erythrit+bio",
    "süßungsmittel": "xylit+birkenzucker",
    "aspartam": "stevia+tropfen+bio",
    "zucker": "kokosblütenzucker",
    
    # Farben
    "farbstoff": "natürliche+lebensmittelfarbe",
    "färben": "färbende+lebensmittel",
    "karmin": "vegane+lebensmittelfarbe",
    "azo": "natürliche+backzutaten",

    # Geschmacksverstärker
    "geschmacksverstärker": "gewürze+ohne+geschmacksverstärker",
    "glutamat": "gemüsebrühe+hefeextraktfrei",
    "hefe": "liebstöckel+bio",
    
    # Konservierung
    "konservierungsstoff": "einmachgläser+weck", # Idee: Selbst haltbar machen
    "konservierung": "fermentierset",
    "nitrit": "rauchsalz+bio",
    "pökelsalz": "meersalz+unraffiniert",
    
    # Bindemittel/Textur
    "verdickungsmittel": "guarkernmehl+bio",
    "geliermittel": "agar+agar+bio",
    "emulgator": "sonnenblumenlecithin+bio",
    
    # Überzugsmittel (z.B. Vaseline)
    "überzugsmittel": "bienenwachstücher", # Natürliche Alternative für Haltbarkeit
    "wachs": "bienenwachs+pastillen",
    "vaseline": "bio+kokosöl", # Natürliche Fett-Alternative
    "paraffin": "bienenwachstücher",
    
    # Säure
    "säuerungsmittel": "apfelessig+naturtrüb",
}

# --- CSS DESIGN ---
css_styles = """
<style>
    :root { 
        --primary: #10b981; --primary-dark: #059669;
        --bg: #f9fafb; --text: #1f2937; --card-bg: #ffffff; --border: #e5e7eb;
        --amazon: #ff9900;
    }
    body { font-family: 'Inter', system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; margin: 0; display: flex; flex-direction: column; min-height: 100vh; }
    
    nav { background: white; border-bottom: 1px solid var(--border); padding: 1rem 0; position: sticky; top: 0; z-index: 50; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
    .nav-container { max-width: 1000px; margin: 0 auto; padding: 0 1.5rem; display: flex; justify-content: space-between; align-items: center; }
    .logo { font-weight: 800; font-size: 1.25rem; color: var(--primary-dark); text-decoration: none; }
    .nav-links a { color: #6b7280; text-decoration: none; font-size: 0.9rem; font-weight: 500; margin-left: 1.5rem; }

    .container { max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem; width: 100%; box-sizing: border-box; flex: 1; }
    
    .hero { text-align: center; padding: 4rem 1rem 3rem 1rem; background: white; border-bottom: 1px solid var(--border); }
    .hero h1 { font-size: 2.5rem; margin-bottom: 0.5rem; letter-spacing: -0.025em; color: #111827; }
    .search-box { width: 100%; max-width: 500px; padding: 16px 24px; border: 2px solid #e5e7eb; border-radius: 100px; font-size: 1.1rem; outline: none; transition: all 0.2s; display: block; margin: 2rem auto 0 auto; }
    .search-box:focus { border-color: var(--primary); box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.1); }

    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 2rem; }
    .card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; text-decoration: none; color: inherit; transition: all 0.2s; display: flex; flex-direction: column; height: 100%; }
    .card:hover { transform: translateY(-3px); box-shadow: 0 10px 20px -5px rgba(0,0,0,0.1); border-color: var(--primary); }
    
    .card-header { display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem; }
    .e-code { font-size: 0.85rem; font-weight: 700; color: #9ca3af; text-transform: uppercase; }
    .card-title { font-size: 1.1rem; font-weight: 700; color: #111827; margin: 0.2rem 0 0.5rem 0; }
    .card-intro { font-size: 0.9rem; color: #6b7280; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }

    .badge { display: inline-flex; align-items: center; padding: 2px 10px; border-radius: 99px; font-size: 0.75rem; font-weight: 700; }
    .bg-green { background-color: #d1fae5; color: #065f46; }
    .bg-orange { background-color: #ffedd5; color: #9a3412; }
    .bg-red { background-color: #fee2e2; color: #991b1b; }
    
    .detail-header { background: white; border-bottom: 1px solid var(--border); padding: 3rem 0; text-align: center; }
    .detail-title { font-size: 2.5rem; font-weight: 800; color: #111827; margin: 0.5rem 0; }
    
    .section-card { background: white; border-radius: 16px; border: 1px solid var(--border); padding: 2rem; margin-bottom: 2rem; }
    .section-title { font-size: 1.25rem; font-weight: 700; color: #111827; margin-bottom: 1rem; display: flex; align-items: center; gap: 8px; }
    
    .info-list li { padding: 0.75rem 0; border-bottom: 1px solid #f3f4f6; display: flex; justify-content: space-between; }
    .info-list li:last-child { border-bottom: none; }
    
    /* AFFILIATE BOX */
    .affiliate-box { background: linear-gradient(135deg, #fffbeb 0%, #fff7ed 100%); border: 1px solid #fed7aa; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem; display: flex; align-items: center; gap: 1.5rem; position: relative; overflow: hidden; }
    .affiliate-icon { font-size: 2rem; background: white; width: 60px; height: 60px; display: flex; justify-content: center; align-items: center; border-radius: 50%; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .affiliate-content h4 { margin: 0 0 0.5rem 0; color: #9a3412; font-size: 1.1rem; }
    .affiliate-content p { margin: 0; font-size: 0.95rem; color: #4b5563; }
    .affiliate-btn { background: #f97316; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 0.9rem; display: inline-block; margin-top: 0.8rem; transition: background 0.2s; }
    .affiliate-btn:hover { background: #ea580c; }
    
    .share-buttons { display: flex; gap: 10px; justify-content: center; margin-top: 2rem; }
    .share-btn { padding: 8px 16px; border-radius: 6px; text-decoration: none; font-size: 0.85rem; font-weight: 500; color: white; }
    .share-wa { background: #25D366; }
    .share-tw { background: #1DA1F2; }

    footer { background: white; border-top: 1px solid var(--border); padding: 2rem 0; text-align: center; color: #9ca3af; margin-top: auto; }
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
    rating = item.get('health_check', {}).get('rating', 'Unbekannt')
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"Ist {item['name']} gesund oder schädlich?",
        "description": item.get('meta_description', ''),
        "author": {"@type": "Organization", "name": SITE_NAME},
        "publisher": {"@type": "Organization", "name": SITE_NAME, "logo": {"@type": "ImageObject", "url": f"{BASE_URL}/logo.png"}},
        "mainEntity": {
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": f"Ist {item.get('name')} vegan?",
                    "acceptedAnswer": {"@type": "Answer", "text": "Ja." if item.get('dietary_info', {}).get('is_vegan') else "Nein."}
                },
                {
                    "@type": "Question",
                    "name": f"Ist {item.get('name')} gesund?",
                    "acceptedAnswer": {"@type": "Answer", "text": item.get('health_check', {}).get('details', '')}
                }
            ]
        }
    }
    return json.dumps(schema)

# --- INTELLIGENTE SUCHE ---
def get_amazon_query(item):
    # Wir kombinieren alle Texte, um Keywords zu finden
    full_text = (str(item.get('name', '')) + " " + 
                 str(item.get('usage', '')) + " " + 
                 str(item.get('intro_hook', ''))).lower()
    
    # Prüfen, ob wir ein passendes Keyword finden
    for keyword, query in AFFILIATE_MAPPINGS.items():
        if keyword in full_text:
            return query
            
    # Fallback, wenn nichts passt
    return "bio+lebensmittel+ohne+zusatzstoffe"

def get_affiliate_html(item):
    if not SHOW_ADS: return ""
    
    rating = item.get('health_check', {}).get('rating', 'Unbekannt')
    risk_color = get_risk_class(rating)
    
    if risk_color in ['bg-orange', 'bg-red']:
        # Hier wird die magische Query generiert
        query = get_amazon_query(item)
        link = f"https://www.amazon.de/s?k={query}&tag={AMAZON_PARTNER_TAG}"
        
        return f"""
        <div class="affiliate-box">
            <div class="affiliate-icon">🌿</div>
            <div class="affiliate-content">
                <h4>Gesunde Alternative gesucht?</h4>
                <p>Dieser Stoff ist umstritten. Entdecken Sie natürliche Alternativen für "{item.get('name')}".</p>
                <a href="{link}" target="_blank" rel="nofollow" class="affiliate-btn">Passende Bio-Produkte bei Amazon ↗</a>
                <div style="font-size:0.7rem; color:#9ca3af; margin-top:5px;">Anzeige</div>
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
                <a href="index.html">Übersicht</a>
                <a href="impressum.html">Rechtliches</a>
            </div>
        </div>
    </nav>
    """

# --- BUILD ---
def build():
    if os.path.exists(OUTPUT_DIR): shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f: additives = json.load(f)
        print(f"✅ {len(additives)} Einträge geladen.")
    except Exception as e:
        print(f"❌ Fehler: {e}"); return

    sitemap_urls = []
    
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
                <div class="section-card"><h2 class="section-title">💡 Überblick</h2><p style="font-size: 1.1rem; color: #4b5563;">{item.get('intro_hook')}</p></div>
                <div class="grid" style="margin-top:0; margin-bottom: 2rem;">
                    <div class="section-card" style="margin-bottom:0;"><h3 class="section-title">🏥 Gesundheits-Check</h3><p>{item.get('health_check', {}).get('details')}</p></div>
                    <div class="section-card" style="margin-bottom:0;"><h3 class="section-title">🥗 Ernährung</h3><ul class="info-list"><li><span class="info-label">Vegan?</span> <span class="info-value">{"Ja 🌱" if item.get('dietary_info', {}).get('is_vegan') else "Nein 🥩"}</span></li><li><span class="info-label">Glutenfrei?</span> <span class="info-value">{"Ja 🍞" if item.get('dietary_info', {}).get('is_gluten_free') else "Nein 🌾"}</span></li><li><span class="info-label">Herkunft</span> <span class="info-value" style="text-align:right; font-size:0.9rem;">{item.get('dietary_info', {}).get('origin_explanation')}</span></li></ul></div>
                </div>
                <div class="section-card"><h3 class="section-title">🏭 Verwendung</h3><p>{item.get('usage')}</p></div>
                <div class="section-card" style="border-left: 4px solid var(--primary);"><h3 class="section-title">🏁 Fazit</h3><p>{item.get('conclusion')}</p></div>
                <div class="share-buttons">
                    <a href="https://api.whatsapp.com/send?text={BASE_URL}/{filename}" target="_blank" class="share-btn share-wa">Per WhatsApp teilen</a>
                </div>
                <div style="text-align:center; margin-top:2rem;"><a href="index.html" style="color:var(--primary); font-weight:600; text-decoration:none;">← Zurück zur Übersicht</a></div>
            </main>
            <footer><p>&copy; {datetime.now().year} {SITE_NAME}</p><a href="impressum.html">Impressum</a> • <a href="datenschutz.html">Datenschutz</a></footer>
        </body>
        </html>
        """
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f: f.write(html)
        sitemap_urls.append(f"{BASE_URL}/{filename}")

    # INDEX
    cards_html = ""
    for item in additives:
        slug = clean_slug(f"{item.get('e_number', '')}-{item.get('name', '')}")
        rating = item.get('health_check', {}).get('rating', '')
        cards_html += f"""<a href="{slug}.html" class="card filter-item"><div class="card-header"><span class="e-code">{item.get('e_number')}</span><span class="badge {get_risk_class(rating)}">{rating}</span></div><h3 class="card-title">{item.get('name')}</h3><p class="card-intro">{item.get('intro_hook')}</p></a>"""
    
    index_html = f"""<!DOCTYPE html><html lang="de"><head><title>{SITE_NAME}</title><meta name="viewport" content="width=device-width, initial-scale=1">{css_styles}<script>function filterList() {{ var input = document.getElementById("search"); var filter = input.value.toUpperCase(); var cards = document.getElementsByClassName("filter-item"); for (var i = 0; i < cards.length; i++) {{ var txt = cards[i].innerText; if (txt.toUpperCase().indexOf(filter) > -1) {{ cards[i].style.display = "flex"; }} else {{ cards[i].style.display = "none"; }} }} }}</script></head><body>{build_nav()}<div class="hero"><h1>E-Nummern Check</h1><p>Die transparente Enzyklopädie.</p><input type="text" id="search" onkeyup="filterList()" class="search-box" placeholder="🔍 Suchen..."></div><main class="container"><div class="grid">{cards_html}</div></main><footer><p>&copy; {datetime.now().year} {SITE_NAME}</p><a href="impressum.html">Impressum</a></footer></body></html>"""
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f: f.write(index_html)
    
    # LEGAL
    legal_dummy = f"<html><head><title>Rechtliches</title>{css_styles}</head><body>{build_nav()}<main class='container'><div class='section-card'><h1>Impressum</h1><p>{IMPRESSUM_NAME}</p></div></main></body></html>"
    with open(os.path.join(OUTPUT_DIR, "impressum.html"), "w", encoding="utf-8") as f: f.write(legal_dummy)
    with open(os.path.join(OUTPUT_DIR, "datenschutz.html"), "w", encoding="utf-8") as f: f.write(legal_dummy)
    
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join([f'  <url><loc>{u}</loc></url>\n' for u in sitemap_urls]) + '</urlset>'
    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f: f.write(sitemap_xml)

    print(f"✅ Version 2.1 fertig: Smarte Affiliate Links generiert!")

if __name__ == "__main__":
    build()
