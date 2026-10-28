import json
import os
import re

CATALOG_PATH = 'catalogo_completo.html'
METADATA_PATH = 'metadata.json'

def update_catalog():
    with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Get new artworks from 39 MATERDIGISSE
    with open(METADATA_PATH, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    new_artworks = [art for id, art in metadata.items() if isinstance(art, dict) and art.get('category') == "39 MATERDIGISSE"]
    new_artworks.sort(key=lambda x: x['id'])
    
    current_total = 368
    new_total = current_total + len(new_artworks)
    
    # 2. Update existing footers (X / 368 -> X / 380)
    content = content.replace('/ 368</footer>', f'/ {new_total}</footer>')
    
    # 3. Generate new pages HTML
    new_pages_html = ""
    for i, art in enumerate(new_artworks, current_total + 1):
        page_html = f"""
    <div class="page artwork-page">
        <div class="artwork-image-container">
            <img src="{art['src']}" class="artwork-image" alt="{art['title']}">
        </div>
        <div class="artwork-info">
            <h3 class="artwork-title">{art['title']}</h3>
            <div class="artwork-meta">Colección: {art['category']}</div>
            <p class="artwork-desc">{art['description']}</p>
            <p class="tech-info">{art['tech_info']}</p>
        </div>
        <footer>{i} / {new_total}</footer>
    </div>
"""
        new_pages_html += page_html

    # 4. Insert new pages before </body>
    content = content.replace('</body>', f'{new_pages_html}\n</body>')
    
    # 5. Update generation date
    import datetime
    today = datetime.date.today().strftime("%d/%m/%Y")
    content = re.sub(r'Generado el \d{2}/\d{2}/\d{4}', f'Generado el {today}', content)

    # 6. Cleanup SELLOS_MAGICOS to SELLOS MAGICOS
    content = content.replace('Colección: SELLOS_MAGICOS', 'Colección: SELLOS MAGICOS')

    with open(CATALOG_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Catalog updated: Added {len(new_artworks)} pages. New total: {new_total}")

if __name__ == "__main__":
    update_catalog()
