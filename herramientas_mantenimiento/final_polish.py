import json
import os
import re

DATA_JS_PATH = 'js/data.js'
METADATA_PATH = 'metadata.json'

def final_polish():
    # 1. Update data.js
    with open(DATA_JS_PATH, 'r', encoding='utf-8') as f:
        js_content = f.read()

    # Rename category everywhere
    js_content = js_content.replace('1000 SELLOS MAGICOS', 'SELLOS MAGICOS')
    
    # Remove cover_book from artworkData
    js_content = re.sub(r'\{\s*"id":\s*"cover_book".*?\},', '', js_content, flags=re.DOTALL)
    js_content = re.sub(r'\{\s*"id":\s*"cover_book".*?\}', '', js_content, flags=re.DOTALL)

    # Update prices and offer in description for SELLOS MAGICOS
    offer_text = "\\n\\n🎁 OFERTA: 1,10€ (unidad) / Pack 5: 3,90€"
    
    def update_stamp_data(match):
        block = match.group(0)
        block = re.sub(r'"price":\s*".*?"', '"price": "1,10€"', block)
        desc_match = re.search(r'"description":\s*"(.*?)"', block)
        if desc_match:
            desc_content = desc_match.group(1)
            if "OFERTA" not in desc_content:
                new_desc = desc_content + offer_text
                block = block.replace(desc_content, new_desc)
        return block

    js_content = re.sub(r'\{[^{}]*?"category":\s*"SELLOS MAGICOS"[^{}]*?\}', update_stamp_data, js_content, flags=re.DOTALL)

    with open(DATA_JS_PATH, 'w', encoding='utf-8') as f:
        f.write(js_content)

    # 2. Update metadata.json
    with open(METADATA_PATH, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    if 'cover_book' in metadata:
        del metadata['cover_book']

    for key, art in metadata.items():
        if isinstance(art, dict):
            if art.get('category') in ['1000 SELLOS MAGICOS', 'SELLOS MAGICOS', 'SELLOS_MAGICOS']:
                art['category'] = 'SELLOS MAGICOS'
                art['price'] = '1,10€'
                if "OFERTA" not in art.get('description', ''):
                    art['description'] = art.get('description', '') + "\n\n🎁 OFERTA: 1,10€ (unidad) / Pack 5: 3,90€"

    with open(METADATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    print("Final polish complete (fixed).")

if __name__ == "__main__":
    final_polish()
