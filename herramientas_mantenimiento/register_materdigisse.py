import json
import os
import re

ASSETS_DIR = 'assets/39MATERDIGISSE'
DATA_JS_PATH = 'js/data.js'
METADATA_PATH = 'metadata.json'

def register_materdigisse():
    # 1. Load existing metadata
    with open(METADATA_PATH, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    files = [f for f in os.listdir(ASSETS_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    files.sort()
    
    # Find existing IDs for this category
    existing_srcs = {item['src'] for id, item in metadata.items() if isinstance(item, dict) and item.get('category') == "39 MATERDIGISSE"}
    
    # Find the last ID used for this category
    max_id = 0
    for id_key in metadata.keys():
        if id_key.startswith("39materdigisse_"):
            try:
                num = int(id_key.split('_')[1])
                if num > max_id: max_id = num
            except: pass

    new_entries = []
    category = "39 MATERDIGISSE"
    
    for filename in files:
        src_path = f"assets/39MATERDIGISSE/{filename}"
        if src_path in existing_srcs:
            continue # Already registered
            
        max_id += 1
        clean_name = os.path.splitext(filename)[0]
        title = clean_name.replace('_', ' ').replace('-', ' ').replace(' plus', '').title()
        item_id = f"39materdigisse_{max_id:03d}"
        
        entry = {
            "id": item_id,
            "title": title,
            "category": category,
            "src": src_path,
            "description": "Exploración de la materia digital y energía vortical. Sinergia entre figura y trazo rítmico.",
            "size": "Consultar",
            "price": "19,99€",
            "tech_info": "Técnica MATERDIGISSE (Digital Impasto)",
            "sold": False
        }
        new_entries.append(entry)

    if not new_entries:
        print("No new artworks found to register.")
        return

    # Update metadata.json
    for entry in new_entries:
        metadata[entry['id']] = entry
    
    with open(METADATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    # Update data.js
    with open(DATA_JS_PATH, 'r', encoding='utf-8') as f:
        js_content = f.read()

    # Append artworks to artworkData array
    new_js_entries = ",\n".join([f'        {json.dumps(entry, ensure_ascii=False)}' for entry in new_entries])
    
    # Insert before the last ];
    js_content = re.sub(r'(\s*)(\];\s*)$', f',\n{new_js_entries}\\1\\2', js_content)

    with open(DATA_JS_PATH, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"Registered {len(new_entries)} NEW artworks in {category}")

if __name__ == "__main__":
    register_materdigisse()
