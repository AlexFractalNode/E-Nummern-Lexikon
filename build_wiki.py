import pandas as pd
import os
import shutil
from datetime import datetime

# --- KONFIGURATION ---
OUTPUT_DIR = 'site_output'
DATA_FILE = 'additives.csv'
SITE_NAME = "E-Check Lexikon 📘"
BASE_URL = "https://[AlexFractalNode].github.io/[E-Nummern Lexikon]"

# IMPRESSUM
IMPRESSUM_NAME = "Alexander Heinze"
IMPRESSUM_ADRESSE = "Am Fuchsgraben 28, 08056 Zwickau"

# --- 1. DATEN LADEN ---
print("📚 Lade E-Nummern Datenbank...")

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    print(f"✅ {len(df)} Einträge aus '{DATA_FILE}' geladen.")
else:
    print("⚠️ Keine CSV gefunden. Erstelle Demo-Daten...")
    # Demo-Daten, damit der Code sofort funktioniert
    data = {
        'code': ['E100', 'E120', 'E330', 'E621', 'E951'],
        'name': ['Kurkumin', 'Echtes Karmin', 'Zitronensäure', 'Mononatriumglutamat', 'Aspartam'],
        'risk': ['Unbedenklich', 'Bedenklich', 'Unbedenklich', 'Sehr Bedenklich', 'Umstritten'],
        'category': ['Farbstoff', 'Farbstoff', 'Säuerungsmittel', 'Geschmacksverstärker', 'Süßstoff'],
        'description': [
            'Natürlicher Farbstoff aus der Kurkuma-Wurzel.',
            'Roter Farbstoff, der aus Schildläusen gewonnen wird. Nicht vegan.',
            'Kommt in Zitrusfrüchten vor, wird aber oft industriell durch Schimmelpilze hergestellt.',
            'Kann bei empfindlichen Personen Kopfschmerzen auslösen (China-Restaurant-Syndrom).',
            'Süßstoff, der oft in Light-Produkten verwendet wird. Steht im Verdacht, Migräne auszulösen.'
        ],
        'vegan': ['Ja', 'Nein', 'Ja', 'Ja', 'Ja']
    }
    df = pd.DataFrame(data)

# Daten bereinigen
df = df.fillna('')

# --- 2. CSS DESIGN (Modern & Scientific) ---
css_styles = """
<style>
    :root { --primary: #0ea5e9; --bg: #f8fafc; --text: #0f172a; --card: #ffffff; }
    body { font-family: 'Inter', system-ui, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; margin: 0; }
    
    nav { background: white; border-bottom: 1px solid #e2e8f0; padding: 1rem 0; position: sticky; top: 0; z-index: 10; }
    .container { max-width: 900px; margin: 0 auto; padding: 0 1.5rem; }
    .nav-flex { display: flex; justify-content: space-between; align-items: center; }
    .logo { font-weight: 800; font-size: 1.3rem; color: var(--primary); text-decoration: none; }
    
    .hero { text-align: center; padding: 4rem 1rem; }
    .hero h1 { font-size: 2.5rem; margin-bottom: 0.5rem; letter-spacing: -1px; }
    
    /* Search Bar */
    .search-box { width: 100%; max-width: 500px; padding: 15px; border: 1px solid #cbd5e1; border-radius: 12px; font-size: 1rem; margin: 0 auto; display: block; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }

    /* Grid */
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 2rem; }
    
    /* Cards */
    .card { background: var(--card); padding: 1.5rem; border-radius: 12px; border: 1px solid #e2e8f0; text-decoration: none; color: inherit; transition: transform 0.2s; display: block; }
    .card:hover { transform: translateY(-4px); border-color: var(--primary); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
    
    .e-code { font-size: 1.5rem; font-weight: 800; color: var(--text); }
    .e-name { color: #64748b; font-weight: 500; margin-bottom: 1rem; display: block; }
    
    /* Badges */
    .badge { display: inline-block; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: bold; }
    .risk-safe { background: #dcfce7; color: #166534; }
    .risk-medium { background: #fef9c3; color: #854d0e; }
    .risk-high { background: #fee2e2; color: #991b1b; }
    
    /* Detail Page */
    .detail-header { background: white; padding: 3rem 0; border-bottom: 1px solid #e2e8f0; text-align: center; }
    .detail-content { background: white; padding: 2rem; border-radius: 12px; margin-top: -2rem; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
    
    .info-row { display: flex; justify-content: space-between; padding: 1rem 0; border-bottom: 1px solid #f1f5f9; }
    .info-label { font-weight: 600; color: #64748b; }
    
    footer { text-align: center; margin-top: 4rem; padding: 2rem; color: #94a3b8; font-size: 0.9rem; }
    a { color: inherit; }
</style>
"""

# --- 3. TEMPLATES ---
def get_risk_class(risk_text):
    r = str(risk_text).lower()
    if 'unbedenklich' in r: return 'risk-safe'
    if 'sehr bedenklich' in r: return 'risk-high'
    return 'risk-medium'

def build_nav():
    return f"""
    <nav>
        <div class="container nav-flex">
            <a href="index.html" class="logo">📘 E-Lexikon</a>
            <div>
                <a href="impressum.html" style="font-size:0.9rem; margin-left:1rem;">Rechtliches</a>
            </div>
        </div>
    </nav>
    """

# --- 4. SEITEN BAUEN ---
if os.path.exists(OUTPUT_DIR): shutil.rmtree(OUTPUT_DIR)
os.makedirs(OUTPUT_DIR)

# A) Detailseiten
for index, row in df.iterrows():
    slug = row['code'].lower().replace(" ", "")
    filename = f"{slug}.html"
    
    risk_badge = f"<span class='badge {get_risk_class(row['risk'])}'>{row['risk']}</span>"
    
    html = f"""
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{row['code']} - {row['name']} | Ist das schädlich?</title>
        <meta name="description" content="Alles über {row['code']} ({row['name']}). Risiken, Herkunft und ob es vegan ist.">
        {css_styles}
    </head>
    <body>
        {build_nav()}
        
        <header class="detail-header">
            <div class="container">
                <span style="color:#64748b; font-weight:600; text-transform:uppercase;">{row['category']}</span>
                <h1 style="font-size:3.5rem; margin:0.5rem 0;">{row['code']}</h1>
                <h2 style="font-weight:400; color:#475569; margin-top:0;">{row['name']}</h2>
                {risk_badge}
            </div>
        </header>
        
        <main class="container">
            <div class="detail-content">
                <h3>Was ist das?</h3>
                <p style="font-size:1.1rem;">{row['description']}</p>
                
                <div style="margin-top:2rem;">
                    <div class="info-row">
                        <span class="info-label">Kategorie</span>
                        <span>{row['category']}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Vegan?</span>
                        <span>{row['vegan']}</span>
                    </div>
                    <div class="info-row">
                        <span class="info-label">Risikoeinschätzung</span>
                        <span>{row['risk']}</span>
                    </div>
                </div>
                
                <div style="margin-top:2rem; text-align:center;">
                    <a href="index.html" style="text-decoration:underline; color:#0ea5e9;">← Zurück zur Übersicht</a>
                </div>
            </div>
        </main>
        
        <footer>
            <p>&copy; {datetime.now().year} {SITE_NAME}</p>
            <a href="impressum.html">Impressum</a> • <a href="datenschutz.html">Datenschutz</a>
        </footer>
    </body>
    </html>
    """
    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f: f.write(html)

# B) Index Seite
cards_html = ""
for index, row in df.iterrows():
    slug = row['code'].lower().replace(" ", "")
    risk_class = get_risk_class(row['risk'])
    cards_html += f"""
    <a href="{slug}.html" class="card filter-item">
        <div style="display:flex; justify-content:space-between;">
            <span class="e-code">{row['code']}</span>
            <span class="badge {risk_class}">{row['risk']}</span>
        </div>
        <span class="e-name">{row['name']}</span>
        <div style="font-size:0.9rem; color:#64748b;">{row['category']}</div>
    </a>
    """

index_html = f"""
<!DOCTYPE html>
<html lang="de">
<head>
    <title>{SITE_NAME} - Alle Zusatzstoffe erklärt</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {css_styles}
    <script>
    function filterList() {{
        var input = document.getElementById("search");
        var filter = input.value.toUpperCase();
        var cards = document.getElementsByClassName("filter-item");
        
        for (var i = 0; i < cards.length; i++) {{
            var txt = cards[i].innerText;
            if (txt.toUpperCase().indexOf(filter) > -1) {{
                cards[i].style.display = "";
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
        <h1>Was steckt in deinem Essen?</h1>
        <p style="color:#64748b; font-size:1.2rem;">Die große Enzyklopädie der Lebensmittel-Zusatzstoffe.</p>
        <br>
        <input type="text" id="search" onkeyup="filterList()" class="search-box" placeholder="🔍 Suche nach E120, Aspartam, Farbstoff...">
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
with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f: f.write(index_html)

# C) Rechtstexte (Platzhalter)
legal_html = f"""<html><head><title>Rechtliches</title>{css_styles}</head><body>{build_nav()}<main class='container' style='margin-top:4rem'><h1>Impressum & Datenschutz</h1><p>{IMPRESSUM_NAME}<br>{IMPRESSUM_ADRESSE}</p><a href='index.html'>Zurück</a></main></body></html>"""
with open(os.path.join(OUTPUT_DIR, "impressum.html"), "w", encoding="utf-8") as f: f.write(legal_html)
with open(os.path.join(OUTPUT_DIR, "datenschutz.html"), "w", encoding="utf-8") as f: f.write(legal_html)

print(f"✅ Lexikon generiert! {len(df)} Seiten im Ordner '{OUTPUT_DIR}' erstellt.")