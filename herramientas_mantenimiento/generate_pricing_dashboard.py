import json
import os

# Updated to use the new premium pricing giclée print strategy
METADATA_FILE = "metadata.json"
OUTPUT_FILE = "documentacion_y_planificacion/resumen_precios_excel.html"

# Load metadata.json
with open(METADATA_FILE, "r", encoding="utf-8") as f:
    metadata = json.load(f)

# TIER_MAPPING maps old categories to the new premium tiers:
# Tiers:
# - Nivel 3 (Premium) [old Nivel 1 Lujo]: 1.500€ – 3.000€ (Proposed base: 1.800€, 15 copies)
# - Nivel 2 (Medio) [old Nivel 2 Autor]: 500€ – 1.200€ (Proposed base: 750€, 30 copies)
# - Nivel 1 (Acceso) [old Nivel 3/4]: 150€ – 400€ (Proposed base: 250€ for line art, 180€ for applied art, 30 copies)
# - Especial: Numismática (Sellos): En estudio
TIER_MAPPING = {
    # Nivel 3: Premium (1.800€) - 15 copias
    "00 EDUSSE": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "12 CRISTAL CÚBICO": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "12 CRISTAL C\ufffdBICO": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "12 CRISTAL CBICO": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "22 NEO-LUMINA": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "22NEO-LUMINA": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "23 TRIDIM-BURST": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "23TRIDIM-BURST": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "39 MATERDIGISSE": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "40 MECHPASTOSSE": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "41 GESSOLUX": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "42 GESSOLUX EXTREMUM": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "44 GESSOLUX AZURITE": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "45 GESSOLUX IRIS": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "46 ESPATAC-EXTREME": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "46ESPATAC-EXTREME": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "48BESSELUXY_L": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "50 NEO FAUVE": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "51 NEO-CLASICC": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "51NEO-CLASICC": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "49 ARTE CIBERNETICO NATURE": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-CIBER", "15"),
    "52 EDUSSE_CLASSIC": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "52 EDUSSE CLASSIC": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "52EDUSSE_CLASSIC": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "53 MONETESSE": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),
    "53MONETESSE": ("Nivel 3: Premium", "1.800,00", "badge-n1", "Ed. Limitada (15 copias)", "EA-PREM", "15"),

    # Nivel 2: Medio (750€) - 30 copias
    "01 EXP NEOCIRC": ("Nivel 2: Medio", "750,00", "badge-n2", "Ed. Limitada (30 copias)", "EA-MED", "30"),
    "02 CUBESSE STILO": ("Nivel 2: Medio", "750,00", "badge-n2", "Ed. Limitada (30 copias)", "EA-MED", "30"),
    "03 EXPNEOPLUS": ("Nivel 2: Medio", "750,00", "badge-n2", "Ed. Limitada (30 copias)", "EA-MED", "30"),
    "08BORACARBON": ("Nivel 2: Medio", "750,00", "badge-n2", "Ed. Limitada (30 copias)", "EA-MED", "30"),
    "10OLEOCUBBO": ("Nivel 2: Medio", "750,00", "badge-n2", "Ed. Limitada (30 copias)", "EA-MED", "30"),
    "15CUBESSEPLUS": ("Nivel 2: Medio", "750,00", "badge-n2", "Ed. Limitada (30 copias)", "EA-MED", "30"),
    "20BORASSIE": ("Nivel 2: Medio", "750,00", "badge-n2", "Ed. Limitada (30 copias)", "EA-MED", "30"),
    "21OCE-BURST": ("Nivel 2: Medio", "750,00", "badge-n2", "Ed. Limitada (30 copias)", "EA-MED", "30"),
    "24BORACARBON MONUMENTOS": ("Nivel 2: Medio", "750,00", "badge-n2", "Ed. Limitada (30 copias)", "EA-MED", "30"),
    "28ESPATAC": ("Nivel 2: Medio", "750,00", "badge-n2", "Ed. Limitada (30 copias)", "EA-MED", "30"),
    "29ESPATAC-MAT": ("Nivel 2: Medio", "750,00", "badge-n2", "Ed. Limitada (30 copias)", "EA-MED", "30"),
    "30OLONATUR-COLOR": ("Nivel 2: Medio", "750,00", "badge-n2", "Ed. Limitada (30 copias)", "EA-MED", "30"),
    "31OLENATUR": ("Nivel 2: Medio", "750,00", "badge-n2", "Ed. Limitada (30 copias)", "EA-MED", "30"),
    "37 IMPASTUS PAINT": ("Nivel 2: Medio", "750,00", "badge-n2", "Ed. Limitada (30 copias)", "EA-MED", "30"),

    # Nivel 1: Acceso (250€) - 30 copias
    "05 PLUMINK": ("Nivel 1: Acceso", "250,00", "badge-n3", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "06 IDE CLASSIC": ("Nivel 1: Acceso", "250,00", "badge-n3", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "07 NEOINK": ("Nivel 1: Acceso", "250,00", "badge-n3", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "09FRACNEO": ("Nivel 1: Acceso", "250,00", "badge-n3", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "11URBANSPHERIC": ("Nivel 1: Acceso", "250,00", "badge-n3", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "16EXPNEO": ("Nivel 1: Acceso", "250,00", "badge-n3", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "17FUZZTESS": ("Nivel 1: Acceso", "250,00", "badge-n3", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "18 ABSTRACTO CONFLUENCIA": ("Nivel 1: Acceso", "250,00", "badge-n3", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "19 FUZZLINE ABS": ("Nivel 1: Acceso", "250,00", "badge-n3", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "25CAPLIVE": ("Nivel 1: Acceso", "250,00", "badge-n3", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "26CARL_LINE": ("Nivel 1: Acceso", "250,00", "badge-n3", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "27LINEVORT": ("Nivel 1: Acceso", "250,00", "badge-n3", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "32SINNOIR": ("Nivel 1: Acceso", "250,00", "badge-n3", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "33MINIGESTPOETIC": ("Nivel 1: Acceso", "250,00", "badge-n3", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "34EXPTERICO": ("Nivel 1: Acceso", "250,00", "badge-n3", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "35PAPERCHIN": ("Nivel 1: Acceso", "250,00", "badge-n3", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "36 LINEART": ("Nivel 1: Acceso", "250,00", "badge-n3", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "47 NEBULÓNICO": ("Nivel 1: Acceso", "250,00", "badge-n3", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "47 NEBULNICO": ("Nivel 1: Acceso", "250,00", "badge-n3", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "47 NEBULÍNICO": ("Nivel 1: Acceso", "250,00", "badge-n3", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "47 NEBULNICO": ("Nivel 1: Acceso", "250,00", "badge-n3", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "54 LUNIORNAT portadas de discos": ("Nivel 1: Acceso", "250,00", "badge-n3", "Ed. Limitada (30 copias)", "EA-ACC", "30"),

    # Nivel 2.5 (Entre Medio y Premium) -> Lo alojamos en Nivel 2 pero con precio y tirada especiales
    "49 ARTE CIBERNÉTICO": ("Nivel 2: Medio", "1.200,00", "badge-n2", "Ed. Limitada (20 copias)", "EA-CIBER", "20"),
    "49 ARTE CIBERNETICO": ("Nivel 2: Medio", "1.200,00", "badge-n2", "Ed. Limitada (20 copias)", "EA-CIBER", "20"),

    # Nivel 4 (anteriormente Nivel 4 Aplicado, ahora también en Acceso con 30 copias)
    "04 APLICC": ("Nivel 1: Acceso", "180,00", "badge-n4", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "13RECTESSE": ("Nivel 1: Acceso", "180,00", "badge-n4", "Ed. Limitada (30 copias)", "EA-ACC", "30"),
    "14TEREXSE": ("Nivel 1: Acceso", "180,00", "badge-n4", "Ed. Limitada (30 copias)", "EA-ACC", "30"),

    # Especial: Numismática (Consultar/Subasta) - En estudio
    "HISTORIA CINCELADA": ("Historia Cincelada", "1.500,00", "badge-special", "Ed. Limitada (5 copias)", "EA-CINC", "5")
}

db_items = []

# Process metadata
for key, val in metadata.items():
    if not isinstance(val, dict):
        continue
    
    category = val.get("category", "")
    title = val.get("title", "")
    src = val.get("src", "")
    item_id = val.get("id", "")
    current_price = val.get("price", "19,99")
    if current_price and not current_price.endswith("€") and not current_price.endswith("EUR") and not current_price.lower() == "consultar":
        current_price = f"{current_price} €"
    elif not current_price:
        current_price = "Sin definir"
    
    actual_price = val.get("price", "")
    
    if val.get("b2b_only"):
        # Explicit B2B Magna item - Super Lujo B2B (1/3 or 1/5 edition - let's set 5 copies)
        db_items.append({
            "id": item_id,
            "title": title,
            "category": category,
            "src": src,
            "current_price": "N/A",
            "tier": "B2B: Super Lujo",
            "proposed_price": "2.500,00",
            "actual_price": actual_price if actual_price != "450€ - 850€" else "2.500,00", # Set default to 2.500,00€
            "badge_class": "badge-b2b",
            "edition": "Ed. Limitada (5 copias)",
            "serial_format": f"EA-B2B-{item_id.upper()}-01/05"
        })
    else:
        # Standard gallery item
        tier_info = TIER_MAPPING.get(category, ("Sin clasificar", "19,99", "badge-muted", "Edición Abierta", "EA", "100"))
        tier_name, prop_price, badge_class, edition, prefix, limit = tier_info
        
        # Special case override for 1850 First Spanish Stamp (sello_magico_033)
        if item_id == "sello_magico_033":
            tier_name = "Historia Cincelada"
            prop_price = "4.000,00"
            badge_class = "badge-special"
            edition = "Ed. Única (1/1 copia)"
            prefix = "EA-CINC"
            limit = "1"
            serial_display = "EA-CINC-033-01/01"
            db_items[-1]["tier"] = tier_name
            db_items[-1]["proposed_price"] = prop_price
            db_items[-1]["badge_class"] = badge_class
            db_items[-1]["edition"] = edition
            db_items[-1]["serial_format"] = serial_display
        
        if limit == "Estudio":
            serial_display = "Pendiente de definir (En Estudio)"
        else:
            serial_display = f"{prefix}-{item_id.replace('_','').upper()}-01/{limit.zfill(2)}"
            
        db_items.append({
            "id": item_id,
            "title": title,
            "category": category,
            "src": src,
            "current_price": current_price,
            "tier": tier_name,
            "proposed_price": prop_price,
            "actual_price": actual_price,
            "badge_class": badge_class,
            "edition": edition,
            "serial_format": serial_display
        })

# Convert list to JSON string for the HTML template
db_items_json = json.dumps(db_items, ensure_ascii=False, indent=4)

# Create the HTML content
html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inventario y Precios — EDUSSE Universe</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --border-color: #e2e8f0;
        }}

        body {{
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 20px;
        }}

        .container {{
            max-width: 1300px;
            margin: 0 auto;
            background: var(--card-bg);
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.025);
            padding: 30px;
            border: 1px solid var(--border-color);
            position: relative;
        }}

        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 20px;
            margin-bottom: 25px;
        }}

        header h1 {{
            margin: 0;
            font-size: 1.8rem;
            font-weight: 700;
            color: #0f172a;
        }}

        header p {{
            margin: 5px 0 0 0;
            color: var(--text-muted);
            font-size: 0.95rem;
        }}

        .top-buttons {{
            display: flex;
            gap: 12px;
        }}

        .btn {{
            padding: 10px 18px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.9rem;
            font-family: inherit;
            cursor: pointer;
            border: none;
            transition: all 0.2s;
        }}

        .btn-primary {{
            background-color: #6366f1;
            color: white;
        }}

        .btn-primary:hover {{
            background-color: #4f46e5;
        }}

        .btn-secondary {{
            background-color: #f1f5f9;
            color: #475569;
            border: 1px solid var(--border-color);
        }}

        .btn-secondary:hover {{
            background-color: #e2e8f0;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 25px;
        }}

        .stat-card {{
            background: #f8fafc;
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .stat-card:hover, .stat-card.active {{
            background: #e0e7ff;
            border-color: #6366f1;
            transform: translateY(-2px);
        }}

        .stat-card h3 {{
            margin: 0 0 5px 0;
            font-size: 0.85rem;
            text-transform: uppercase;
            color: var(--text-muted);
            letter-spacing: 0.05em;
        }}

        .stat-card .value {{
            font-size: 1.4rem;
            font-weight: 700;
            color: #0f172a;
        }}

        .controls {{
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }}

        .search-box {{
            flex: 1;
            position: relative;
        }}

        .search-box input {{
            width: 100%;
            padding: 12px 16px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            font-size: 0.95rem;
            font-family: inherit;
            box-sizing: border-box;
            outline: none;
            transition: border-color 0.2s;
        }}

        .search-box input:focus {{
            border-color: #6366f1;
        }}

        .excel-container {{
            border: 1px solid var(--border-color);
            border-radius: 10px;
            overflow-x: auto;
            max-height: 550px;
            overflow-y: auto;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.9rem;
        }}

        th {{
            background: #f1f5f9;
            color: #475569;
            font-weight: 600;
            padding: 12px 16px;
            position: sticky;
            top: 0;
            z-index: 10;
            border-bottom: 2px solid var(--border-color);
        }}

        td {{
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-color);
            color: #334155;
            vertical-align: middle;
        }}

        tr:hover td {{
            background-color: #f8fafc;
        }}

        .thumb {{
            width: 45px;
            height: 45px;
            object-fit: cover;
            border-radius: 6px;
            border: 1px solid var(--border-color);
            background-color: #f1f5f9;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .badge-b2b {{ background-color: #e0e7ff; color: #4338ca; }}
        .badge-n1 {{ background-color: #fef3c7; color: #b45309; }}
        .badge-n2 {{ background-color: #d1fae5; color: #047857; }}
        .badge-n3 {{ background-color: #ecfeff; color: #0891b2; }}
        .badge-n4 {{ background-color: #f3e8ff; color: #6b21a8; }}
        .badge-special {{ background-color: #fce7f3; color: #be185d; }}
        .badge-muted {{ background-color: #f1f5f9; color: #64748b; }}

        .price-curr {{
            color: var(--text-muted);
            font-size: 0.9rem;
        }}

        .price-input-cell {{
            text-align: right;
        }}

        .price-edit-input {{
            width: 120px;
            padding: 6px 10px;
            border-radius: 6px;
            border: 1px solid var(--border-color);
            font-family: monospace;
            font-weight: 700;
            font-size: 0.95rem;
            text-align: right;
            outline: none;
            transition: all 0.2s;
        }}

        .price-edit-input:focus {{
            border-color: #6366f1;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
            background-color: #faf5ff;
        }}

        .price-edit-input.saved-flash {{
            background-color: #d1fae5 !important;
            border-color: #10b981 !important;
        }}

        .price-edit-input.error-flash {{
            background-color: #fee2e2 !important;
            border-color: #ef4444 !important;
        }}

        .filename-code {{
            font-family: monospace;
            color: #0284c7;
            font-size: 0.8rem;
            background: #f0f9ff;
            padding: 2px 6px;
            border-radius: 4px;
        }}

        .serial-text {{
            font-family: monospace;
            font-size: 0.8rem;
            color: #475569;
        }}

        .info-row {{
            margin-top: 15px;
            font-size: 0.85rem;
            color: var(--text-muted);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        /* Toast notification */
        .toast {{
            position: fixed;
            bottom: 25px;
            right: 25px;
            background: #0f172a;
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            font-size: 0.9rem;
            font-weight: 500;
            z-index: 1000;
            display: none;
            animation: slideUp 0.3s ease-out;
        }}

        @keyframes slideUp {{
            from {{ transform: translateY(100%); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
    </style>
</head>
<body>

<div class="container">
    <header>
        <div>
            <h1>📊 Gestor de Precios Premium (Fine Art & B2B)</h1>
            <p>Escribe el precio que quieras para cualquier obra en la columna **P. Propuesto** y se guardará automáticamente al instante.</p>
        </div>
        <div class="top-buttons">
            <button class="btn btn-secondary" onclick="bulkApplyProposed()">⚡ Aplicar Precios Propuestos a Todas</button>
            <button class="btn btn-primary" onclick="rebuildGallery()">🚀 Publicar Cambios en la Web</button>
        </div>
    </header>

    <!-- Stats and Tiers Filter -->
    <div class="stats-grid">
        <div class="stat-card active" onclick="filterByTier('All', this)">
            <h3>Todas las Obras</h3>
            <div class="value" id="count-all">0</div>
        </div>
        <div class="stat-card" onclick="filterByTier('B2B: Super Lujo', this)">
            <h3>Super Lujo B2B</h3>
            <div class="value" id="count-b2b">0</div>
        </div>
        <div class="stat-card" onclick="filterByTier('Nivel 3: Premium', this)">
            <h3>Nivel 3 (Premium)</h3>
            <div class="value" id="count-n1">0</div>
        </div>
        <div class="stat-card" onclick="filterByTier('Nivel 2: Medio', this)">
            <h3>Nivel 2 (Medio)</h3>
            <div class="value" id="count-n2">0</div>
        </div>
        <div class="stat-card" onclick="filterByTier('Nivel 1: Acceso', this)">
            <h3>Nivel 1 (Acceso)</h3>
            <div class="value" id="count-n3">0</div>
        </div>
        <div class="stat-card" onclick="filterByTier('Especial: Numismática', this)">
            <h3>Numismática</h3>
            <div class="value" id="count-special">0</div>
        </div>
    </div>

    <!-- Controls -->
    <div class="controls">
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="🔍 Buscar por título, ID o estilo de obra..." oninput="filterItems()">
        </div>
    </div>

    <!-- Excel Table -->
    <div class="excel-container">
        <table>
            <thead>
                <tr>
                    <th style="width: 50px;">Min.</th>
                    <th style="width: 120px;">ID de Archivo</th>
                    <th>Título de la Obra</th>
                    <th>Categoría / Estilo</th>
                    <th style="width: 150px;">Clasificación</th>
                    <th style="width: 180px;">Serie Limitada / N° Serie</th>
                    <th style="width: 120px; text-align: right;">Precio Actual (Web)</th>
                    <th style="width: 150px; text-align: right;">P. Propuesto / Nuevo (€)</th>
                </tr>
            </thead>
            <tbody id="tableBody">
                <!-- Dynamically loaded -->
            </tbody>
        </table>
    </div>

    <div class="info-row">
        <span id="showing-text">Mostrando 0 de 0 obras</span>
        <span>EDUSSE Universe — Panel de Control y Administración de Precios</span>
    </div>
</div>

<div class="toast" id="toast">Cambio guardado con éxito</div>

<script>
    // Embed the items compiled from Python
    const artworks = {db_items_json};

    let activeTier = 'All';

    // Calculate totals
    document.getElementById('count-all').innerText = artworks.length;
    document.getElementById('count-b2b').innerText = artworks.filter(item => item.tier === 'B2B: Super Lujo').length;
    document.getElementById('count-n1').innerText = artworks.filter(item => item.tier === 'Nivel 3: Premium').length;
    document.getElementById('count-n2').innerText = artworks.filter(item => item.tier === 'Nivel 2: Medio').length;
    document.getElementById('count-n3').innerText = artworks.filter(item => item.tier === 'Nivel 1: Acceso').length;
    document.getElementById('count-special').innerText = artworks.filter(item => item.tier === 'Especial: Numismática').length;

    function renderTable(data) {{
        const tbody = document.getElementById('tableBody');
        tbody.innerHTML = '';
        
        data.forEach(item => {{
            const tr = document.createElement('tr');
            
            // Thumbnail path logic (handle local paths safely)
            let imgSrc = '../' + item.src;
            // The HTML file is inside documentacion_y_planificacion, so we need to go up one level to reach assets/
            
            let inputVal = item.actual_price;
            
            tr.innerHTML = `
                <td><img class="thumb" src="${{imgSrc}}" onerror="this.src='https://placehold.co/80x80?text=EDUSSE'" alt="miniatura"></td>
                <td><span class="filename-code">${{item.id}}</span></td>
                <td style="font-weight: 500;">${{item.title}}</td>
                <td>${{item.category}}</td>
                <td><span class="badge ${{item.badge_class}}">${{item.tier}}</span></td>
                <td>
                    <div style="font-weight:600; font-size:0.85rem; color:#1e293b;">${{item.edition}}</div>
                    <div class="serial-text" title="Nomenclatura oficial de la firma">${{item.serial_format}}</div>
                </td>
                <td style="text-align: right;" class="price-curr">${{item.current_price}}</td>
                <td class="price-input-cell">
                    <input type="text" class="price-edit-input" value="${{inputVal}}" 
                        onfocus="this.select()"
                        onchange="saveSinglePrice('${{item.id}}', this)">
                </td>
            `;
            tbody.appendChild(tr);
        }});
        
        document.getElementById('showing-text').innerText = `Mostrando ${{data.length}} de ${{artworks.length}} obras`;
    }}

    function filterByTier(tier, element) {{
        activeTier = tier;
        
        // Update active class on cards
        const cards = document.querySelectorAll('.stat-card');
        cards.forEach(card => card.classList.remove('active'));
        element.classList.add('active');
        
        filterItems();
    }}

    function filterItems() {{
        const searchVal = document.getElementById('searchInput').value.toLowerCase();
        
        const filtered = artworks.filter(item => {{
            const matchesSearch = 
                item.title.toLowerCase().includes(searchVal) ||
                item.id.toLowerCase().includes(searchVal) ||
                item.category.toLowerCase().includes(searchVal);
                
            const matchesTier = (activeTier === 'All') || (item.tier === activeTier);
            
            return matchesSearch && matchesTier;
        }});
        
        renderTable(filtered);
    }}

    // Call API to save a single price on change
    function saveSinglePrice(id, inputElement) {{
        const newPrice = inputElement.value.trim();
        
        fetch('/update_price', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{ id: id, price: newPrice }})
        }})
        .then(res => res.json())
        .then(data => {{
            if (data.status === 'success') {{
                inputElement.classList.add('saved-flash');
                showToast("Precio guardado en metadata.json");
                setTimeout(() => inputElement.classList.remove('saved-flash'), 1000);
                
                const artItem = artworks.find(a => a.id === id);
                if (artItem) artItem.actual_price = newPrice;
            }} else {{
                inputElement.classList.add('error-flash');
                showToast("Error al guardar: " + data.message);
                setTimeout(() => inputElement.classList.remove('error-flash'), 2000);
            }}
        }})
        .catch(err => {{
            inputElement.classList.add('error-flash');
            showToast("Error de conexión con el servidor");
            setTimeout(() => inputElement.classList.remove('error-flash'), 2000);
        }});
    }}

    // Bulk apply prices based on proposal
    function bulkApplyProposed() {{
        if (!confirm("¿Seguro que quieres cambiar TODOS los precios de la base de datos a los valores recomendados por nivel? (Ej: Nivel 3 a 1.800€, Nivel 2 a 750€, etc. Esto sobrescribirá los precios actuales).")) return;
        
        fetch('/bulk_apply', {{ method: 'POST' }})
        .then(res => res.json())
        .then(data => {{
            if (data.status === 'success') {{
                showToast("¡Precios de la propuesta aplicados con éxito!");
                setTimeout(() => location.reload(), 1500);
            }} else {{
                alert("Error al aplicar cambios: " + data.message);
            }}
        }});
    }}

    // Rebuild js/data.js and sync to backup
    function rebuildGallery() {{
        showToast("Compilando y actualizando base de datos de la web...");
        fetch('/rebuild', {{ method: 'POST' }})
        .then(res => res.json())
        .then(data => {{
            if (data.status === 'success') {{
                showToast("¡Galería reconstruida y sincronizada!");
            }} else {{
                alert("Error al reconstruir: " + data.message);
            }}
        }});
    }}

    function showToast(message) {{
        const toast = document.getElementById('toast');
        toast.innerText = message;
        toast.style.display = 'block';
        setTimeout(() => {{
            toast.style.display = 'none';
        }}, 3000);
    }}

    // Initial render
    filterItems();
</script>

</body>
</html>
"""

# Write to file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Excel-style pricing dashboard generated successfully at: {OUTPUT_FILE}")
