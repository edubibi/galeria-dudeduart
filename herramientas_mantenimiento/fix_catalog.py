import json
import os
import re

CATALOG_PATH = 'catalogo_completo.html'
METADATA_PATH = 'metadata.json'

def fix_catalog():
    with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove all pages that have "39 MATERDIGISSE"
    # A page is <div class="page artwork-page">...</div>
    # We'll use a more surgical approach: find the first MATERDIGISSE page and remove everything until </body>
    
    # Actually, it's safer to find the marker for the end of the "Old" catalog (stamps)
    # The last stamp was "Velazquez" page 368.
    
    marker = '<footer>368 /'
    parts = content.split(marker)
    if len(parts) > 1:
        # Keep everything up to the end of the 368th page
        header_and_old_pages = parts[0] + marker + parts[1].split('</div>')[0] + '</div>'
        # The split('</div>')[0] + '</div>' captures the rest of the 368th page div
    else:
        print("Marker not found!")
        return

    # 2. Get the correct 16 artworks from metadata.json
    with open(METADATA_PATH, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    new_artworks = [art for id, art in metadata.items() if isinstance(art, dict) and art.get('category') == "39 MATERDIGISSE"]
    new_artworks.sort(key=lambda x: x['id'])
    
    current_total = 368
    new_total = current_total + len(new_artworks)
    
    # Update total in the header part
    header_and_old_pages = header_and_old_pages.replace(f'/ 384</footer>', f'/ {new_total}</footer>')
    # Wait, it might be 380 if I ran it before. I'll use regex for the total.
    header_and_old_pages = re.sub(r'/ \d+</footer>', f'/ {new_total}</footer>', header_and_old_pages)

    # 3. Generate correct new pages
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

    final_content = header_and_old_pages + "\n" + new_pages_html + "\n</body>\n</html>"

    with open(CATALOG_PATH, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"Catalog REPAIRED: 16 correct pages. New total: {new_total}")

if __name__ == "__main__":
    fix_catalog()
