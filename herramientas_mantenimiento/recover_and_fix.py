import re
import os

INPUT_FILE = "behance_showcase_completo.html"

def recover_all_slides():
    print(f"Reading {INPUT_FILE}...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # We will split the file by slide containers
    # Every slide is enclosed in <div class="slide ..."> ... </div>
    # Let's find all slide divs
    slide_matches = re.findall(r'(<!--\s*(?:\d+|DOUBLE COLUMN GROUP).*?-->.*?<div class="slide.*?>.*?</div>\s*</div>)', content, re.DOTALL)
    
    slides = []
    print(f"Found {len(slide_matches)} slide blocks in HTML.")
    
    for block in slide_matches:
        # Check if this is a double column group
        if "DOUBLE COLUMN GROUP" in block:
            # We have two column cards in this block
            # Let's find both cards using regex
            cards = re.findall(r'<div class="double-column-card">.*?</div>\s*</div>', block, re.DOTALL)
            if len(cards) != 2:
                # Fallback if card structure varies slightly
                cards = re.findall(r'<div class="double-column-card">.*?</div>\s*</div>', block + " </div>", re.DOTALL)
                if len(cards) != 2:
                    # Alternative more generous split
                    cards = block.split('<div class="double-column-card">')[1:]
            
            for card in cards[:2]:
                # Parse card elements
                bg_num_m = re.search(r'class="bg-number".*?>(\d+)</div>', card)
                idx_html = bg_num_m.group(1).strip() if bg_num_m else ""
                
                src_m = re.search(r'src="(.*?)"', card)
                img_src = src_m.group(1).strip() if src_m else ""
                
                family_m = re.search(r'FAMILIA:\s*([A-Za-z0-9ÁÉÍÓÚÑáéíóúñ\s_&\-]+)', card)
                family = family_m.group(1).strip() if family_m else ""
                
                title_m = re.search(r'<h3 class="art-title".*?>(.*?)</h3>', card)
                title = title_m.group(1).strip() if title_m else ""
                
                desc_m = re.search(r'class="art-description".*?>(.*?)</p>', card, re.DOTALL)
                desc = desc_m.group(1).strip().replace('\n', ' ') if desc_m else ""
                
                # Clean up description HTML entities
                desc = re.sub(r'\s+', ' ', desc)
                
                slides.append((
                    idx_html,
                    family,  # Use family as style name comment
                    img_src,
                    idx_html,
                    title,
                    family,
                    desc
                ))
        else:
            # Standard or Full-Bleed slide
            # Let's extract comment
            comment_m = re.search(r'<!--\s*(\d+)\s+(.*?)\s*-->', block)
            if not comment_m:
                continue
                
            orig_idx_comment = comment_m.group(1)
            style_name_comment = comment_m.group(2).replace('[MONUMENTAL]', '').replace('[EDITORIAL]', '').strip()
            
            src_m = re.search(r'src="(.*?)"', block)
            img_src = src_m.group(1).strip() if src_m else ""
            
            idx_html = orig_idx_comment
            
            title_m = re.search(r'<h3 class="art-title".*?>(.*?)</h3>', block)
            title = title_m.group(1).strip() if title_m else ""
            
            family_m = re.search(r'FAMILIA:\s*([A-Za-z0-9ÁÉÍÓÚÑáéíóúñ\s_&\-]+)', block)
            family = family_m.group(1).strip() if family_m else ""
            
            desc_m = re.search(r'class="art-description".*?>(.*?)</p>', block, re.DOTALL)
            desc = desc_m.group(1).strip().replace('\n', ' ') if desc_m else ""
            desc = re.sub(r'\s+', ' ', desc)
            
            slides.append((
                orig_idx_comment,
                style_name_comment,
                img_src,
                idx_html,
                title,
                family,
                desc
            ))
            
    print(f"Successfully recovered {len(slides)} slides.")
    for s in slides[:5]:
        print(f"Recovered Style {s[3]}: {s[4]} ({s[5]})")
        
    return slides

if __name__ == "__main__":
    recover_all_slides()
