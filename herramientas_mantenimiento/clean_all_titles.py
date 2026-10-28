import json
import re

METADATA_FILE = 'metadata.json'
DATA_JS_FILE = 'js/data.js'

with open(METADATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Explicit mappings for optimal artistic titles
specific_names = {
    "07neoink_stilo_004": "Casa de Campo Rústica",
    "07neoink_stilo_014": "Talavera 1600 Neo",
    "abuelo_paseando": "Abuelo Paseando",
    "barco_transatlantico_impastus": "Barco Transatlántico",
    "canada_alberta_port1": "Canadá Alberta Puerto I",
    "canada_alberta_port2": "Canadá Alberta Puerto II",
    "canada_alberta_streets": "Canadá Alberta Calles",
    "14terexse_002": "Duna Dorada",
    "01exp_neocirc_005.jpg_202607201144": "Barcos en el Puerto",
    "concentric_circular_strokes_past…_202607201149": "Trazos Concéntricos al Pastel",
    "monasterio_del_escorial_oil_pain…_202607201524": "Monasterio de El Escorial",
    "flock_of_sheep_in_meadow_202607211214": "Rebaño en la Pradera",
    "kasar_ouled_soltane__tunez.jpeg_202607211222": "Ksar Ouled Soltane II"
}

modified = 0
for k, v in data.items():
    if not isinstance(v, dict):
        continue
    old_title = v.get('title', '')
    
    if k in specific_names:
        new_title = specific_names[k]
    else:
        # General cleaning: strip extensions, long timestamp numbers, underscores
        new_title = re.sub(r'\.(jpe?g|png|webp|gif)', '', old_title, flags=re.I)
        new_title = re.sub(r'\s*\d{8,}\b', '', new_title)
        new_title = new_title.replace('_', ' ')
        new_title = re.sub(r'\s+', ' ', new_title).strip()
    
    if new_title != old_title:
        print(f"Modificando [{k}]: '{old_title}' -> '{new_title}'")
        v['title'] = new_title
        modified += 1

print(f"\nTotal títulos actualizados en metadata.json: {modified}")

with open(METADATA_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

# Now update js/data.js
# Construct both galleryData and artworkData cleanly
gallery_dict = {}
artwork_list = []

for k, v in data.items():
    if isinstance(v, dict) and 'id' in v:
        gallery_dict[k] = v
        artwork_list.append(v)

artwork_list.sort(key=lambda x: (x.get("category", ""), x.get("id", "")))

js_content = "const galleryData = " + json.dumps(gallery_dict, indent=4, ensure_ascii=False) + ";\n\n"
js_content += "const artworkData = " + json.dumps(artwork_list, indent=4, ensure_ascii=False) + ";\n"

with open(DATA_JS_FILE, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("¡js/data.js sincronizado y actualizado con éxito!")
