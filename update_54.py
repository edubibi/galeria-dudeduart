import json
import os
import re

files = [
    "Ball in play.jpeg", "Bass stand yeah.jpeg", "Books forever.jpeg", 
    "Bruma.jpg", "Chrome Rhythms.jpg", "Deprisa, ven despacio.jpg", 
    "Dragon lands.jpg", "Feel your dreams.jpeg", "Lotus play.jpeg", 
    "Macao no es Lao.jpeg", "Much time ago.jpg", "Plastic hard.jpg", 
    "Tatum.png", "Without a trace of barbarism.jpeg", "bloody lukas.jpeg"
]

cat_name = "54 LUNIORNAT portadas de discos"
folder = "assets/54 LUNIORNAT/"

# 1. Update metadata.json
meta_path = r"C:\Users\Usuario\.gemini\antigravity-ide\scratch\01_APLICACIONES_Y_WEB\GALERIA_DUDEDUART\metadata.json"
with open(meta_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for file in files:
    name_no_ext = os.path.splitext(file)[0]
    id_key = name_no_ext.lower()
    data[id_key] = {
        "id": id_key,
        "title": name_no_ext.title(),
        "category": cat_name,
        "src": folder + file,
        "description": "Nueva obra añadida recientemente.",
        "price": "1.500,00",
        "size": "Consultar"
    }

with open(meta_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# Update backup as well
backup_path = r"C:\Users\Usuario\.gemini\antigravity-ide\scratch\01_APLICACIONES_Y_WEB\GALERIA_DUDEDUART\metadata.backup.json"
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# 2. Update resumen_precios_excel.html
excel_path = r"C:\Users\Usuario\.gemini\antigravity-ide\scratch\01_APLICACIONES_Y_WEB\GALERIA_DUDEDUART\documentacion_y_planificacion\resumen_precios_excel.html"
with open(excel_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

new_elements = []
for file in files:
    name_no_ext = os.path.splitext(file)[0]
    id_key = name_no_ext.lower()
    title = name_no_ext.title()
    new_elements.append(f"""    {{
        "id": "{id_key}",
        "title": "{title}",
        "category": "{cat_name}",
        "src": "{folder}{file}",
        "current_price": "1.500,00 €",
        "tier": "Nivel 3: Premium",
        "proposed_price": "1.500,00",
        "actual_price": "1.500,00",
        "badge_class": "badge-n1",
        "edition": "Ed. Limitada (15 copias)",
        "serial_format": "EA-PREM-{title.upper()}-01/15"
    }}""")

replacement = "    },\n" + ",\n".join(new_elements) + "\n];"
html_content = re.sub(r'    \}\n\];', replacement, html_content)

with open(excel_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Updates complete.")
