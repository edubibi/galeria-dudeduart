import json
import os
import re

# Paths
METADATA_PATH = 'metadata.json'
DATA_JS_PATH = 'js/data.js'
BACKUP_JS_PATH = 'js/data.js.bak'

def sync_stamps():
    # 1. Load metadata.json
    with open(METADATA_PATH, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    # 2. Backup data.js
    if not os.path.exists(BACKUP_JS_PATH):
        with open(DATA_JS_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(BACKUP_JS_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
    
    with open(DATA_JS_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 3. Add cover_book to metadata if missing
    if 'cover_book' not in metadata:
        metadata['cover_book'] = {
            "id": "cover_book",
            "title": "Libro de los Sellos Mágicos",
            "category": "SELLOS_MAGICOS",
            "src": "assets/SELLOS_MAGICOS/cover_book.png",
            "description": "El tomo ancestral que custodia los secretos de la filatelia mística. Un portal encuadernado en cuero y oro hacia el universo de EDUSSE.",
            "size": "Consultar",
            "price": "Colección",
            "tech_info": "Ver descripción detallada.",
            "sold": False
        }
        # Save metadata update
        with open(METADATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
        print("Added cover_book to metadata.json")

    # 4. Process data.js content
    # Replace "1000 SELLOS MAGICOS" with "SELLOS MAGICOS" everywhere
    content = content.replace("1000 SELLOS MAGICOS", "SELLOS MAGICOS")

    # Parse artworks from content
    # We find the start of the array and replace it with a new one
    start_match = re.search(r'const\s+artworkData\s*=\s*\[', content)
    if not start_match:
        print("Error: Could not find artworkData in data.js")
        return

    # Extract the header (everything before the array content)
    header = content[:start_match.end()]
    
    # We need to preserve the first string entry: "Escribe aquí los datos..."
    # and then build the list of artworks.
    
    # Actually, a safer way to update descriptions is to find each object in the array
    # and update its description if its id starts with "sello_magico_"
    
    # Let's try to update the existing objects in content using regex to find and replace
    # But it's risky with multi-line strings.
    
    # Better approach: 
    # 1. Parse all artworks from data.js
    # 2. Update their fields from metadata.json
    # 3. Add cover_book if missing
    # 4. Reconstruct the file.

    def parse_js_artworks(js_content):
        # Find everything between [ and ];
        match = re.search(r'const\s+artworkData\s*=\s*\[(.*?)\];', js_content, re.DOTALL)
        if not match: return []
        
        array_content = match.group(1)
        # Find all objects { ... }
        # Note: This is a bit naive but should work for the current format.
        art_blocks = re.findall(r'\{(.*?)\}', array_content, re.DOTALL)
        
        artworks = []
        for block in art_blocks:
            # Parse key-value pairs
            art = {}
            for line in block.split('\n'):
                line = line.strip()
                # Match "key": "value", or "key": value,
                kv_match = re.match(r'"(\w+)"\s*:\s*(.*),?', line)
                if kv_match:
                    key = kv_match.group(1)
                    val = kv_match.group(2).strip().rstrip(',')
                    if val.startswith('"') and val.endswith('"'):
                        val = val[1:-1].replace('\\"', '"')
                    elif val == 'true': val = True
                    elif val == 'false': val = False
                    elif val.replace('.','').isdigit(): val = float(val)
                    art[key] = val
            if art: artworks.append(art)
        return artworks

    artworks = parse_js_artworks(content)
    print(f"Parsed {len(artworks)} artworks from data.js")

    # Update artworks
    updated_ids = set()
    new_artworks_list = []
    
    # Add cover_book at the beginning of the stamps if it's not there
    # Or just add it if it doesn't exist in the list.
    
    cover_book_added = False
    
    for art in artworks:
        art_id = art.get('id')
        if art_id in metadata:
            # Sync fields from metadata
            art['description'] = metadata[art_id].get('description', art.get('description'))
            art['category'] = metadata[art_id].get('category', art.get('category'))
            art['title'] = metadata[art_id].get('title', art.get('title'))
            # Fix price if it's "Colección" in metadata but 19,99 in data.js?
            # The user might want to keep the price 19,99 for the web.
            # I'll keep the price from data.js unless it's missing.
        
        if art_id == 'cover_book': cover_book_added = True
        new_artworks_list.append(art)
        updated_ids.add(art_id)

    if not cover_book_added:
        # Add cover_book before the first stamp
        first_stamp_idx = next((i for i, a in enumerate(new_artworks_list) if a.get('id', '').startswith('sello_magico_')), len(new_artworks_list))
        new_artworks_list.insert(first_stamp_idx, metadata['cover_book'])
        print("Inserted cover_book into artworkData")

    # Reconstruct data.js
    # 1. Update categoryCovers
    new_content = re.sub(r'"1000 SELLOS MAGICOS":\s*".*?"', '"SELLOS MAGICOS": "assets/SELLOS_MAGICOS/cover_book.png"', content)
    # Ensure it handles potential spacing/quotes variations
    new_content = new_content.replace('"1000 SELLOS MAGICOS"', '"SELLOS MAGICOS"')
    
    # 2. Reconstruct artworkData array
    # Find the header up to [
    header_match = re.search(r'(const\s+artworkData\s*=\s*\[\s*)', new_content)
    if not header_match:
        print("Could not find array start for reconstruction")
        return
        
    header_part = new_content[:header_match.end()]
    footer_part = "\n];\n" # We'll replace everything after the header
    
    # Build the array items
    items_js = '\n    "Escribe aquí los datos de tus obras. El \'id\' debe coincidir con el nombre del archivo (sin extensión).",'
    for art in new_artworks_list:
        items_js += "\n    {\n"
        for k, v in art.items():
            if isinstance(v, str):
                v_esc = v.replace('"', '\\"')
                items_js += f'        "{k}": "{v_esc}",\n'
            elif isinstance(v, bool):
                items_js += f'        "{k}": {str(v).lower()},\n'
            else:
                items_js += f'        "{k}": {v},\n'
        items_js = items_js.rstrip(',\n') + "\n    },"
    
    items_js = items_js.rstrip(',') # Remove last comma
    
    final_content = header_part + items_js + footer_part
    
    with open(DATA_JS_PATH, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print("Successfully updated js/data.js")

if __name__ == "__main__":
    sync_stamps()
