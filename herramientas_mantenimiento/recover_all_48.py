import re
import os

INPUT_FILE = "behance_showcase_completo.html"

def recover():
    print(f"Reading {INPUT_FILE}...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    slides = []
    current_slide = None
    in_double_column = False
    current_card = None
    
    for line in lines:
        line_str = line.strip()
        
        # Check standard comment
        comment_match = re.search(r'<!--\s*(\d+)\s+(.*?)\s*-->', line_str)
        if comment_match:
            # Save previous slide if fully populated
            if current_slide and current_slide['idx_html'] and current_slide['title'] and current_slide['img_src']:
                slides.append(current_slide)
            if current_card and current_card['idx_html'] and current_card['title'] and current_card['img_src']:
                slides.append(current_card)
                current_card = None
                
            # Start new slide
            current_slide = {
                'orig_idx_comment': comment_match.group(1),
                'style_name_comment': comment_match.group(2).replace('[MONUMENTAL]', '').replace('[EDITORIAL]', '').strip(),
                'img_src': '',
                'idx_html': comment_match.group(1),
                'title': '',
                'family': '',
                'desc': ''
            }
            in_double_column = False
            continue
            
        # Check if we are inside a double column block
        if "layout-double-column" in line_str:
            in_double_column = True
            if current_slide and current_slide['idx_html'] and current_slide['title'] and current_slide['img_src']:
                slides.append(current_slide)
            current_slide = None
            continue
            
        if in_double_column:
            # We are inside a double column slide. Let's look for cards
            if "double-column-card" in line_str:
                if current_card and current_card['idx_html'] and current_card['title'] and current_card['img_src']:
                    slides.append(current_card)
                current_card = {
                    'orig_idx_comment': '',
                    'style_name_comment': '',
                    'img_src': '',
                    'idx_html': '',
                    'title': '',
                    'family': '',
                    'desc': ''
                }
                continue
                
            if current_card:
                # Parse card fields
                if 'class="bg-number"' in line_str:
                    num_m = re.search(r'>(\d+)</div>', line_str)
                    if num_m:
                        current_card['idx_html'] = num_m.group(1).strip()
                        current_card['orig_idx_comment'] = num_m.group(1).strip()
                        
                if 'src="' in line_str and not current_card['img_src']:
                    src_m = re.search(r'src="(.*?)"', line_str)
                    if src_m:
                        current_card['img_src'] = src_m.group(1).strip()
                        
                if 'FAMILIA:' in line_str or 'Familia:' in line_str:
                    fam_m = re.search(r'(?:FAMILIA:|Familia:)\s*([A-Za-z0-9ÁÉÍÓÚÑáéíóúñ\s_&\-]+)', line_str)
                    if fam_m:
                        current_card['family'] = fam_m.group(1).strip()
                        current_card['style_name_comment'] = fam_m.group(1).strip()
                        
                if '<h3' in line_str or 'class="art-title"' in line_str:
                    t_m = re.search(r'<h3.*?>(.*?)</h3>', line_str)
                    if t_m:
                        current_card['title'] = t_m.group(1).strip()
                        
                if 'class="art-description"' in line_str:
                    d_m = re.search(r'class="art-description.*?">(.*?)</p>', line_str)
                    if d_m:
                        current_card['desc'] = d_m.group(1).strip()
                        
        else:
            # Parse normal slide fields
            if current_slide:
                if 'src="' in line_str and not current_slide['img_src']:
                    src_m = re.search(r'src="(.*?)"', line_str)
                    if src_m:
                        current_slide['img_src'] = src_m.group(1).strip()
                        
                if 'FAMILIA:' in line_str or 'Familia:' in line_str:
                    fam_m = re.search(r'(?:FAMILIA:|Familia:)\s*([A-Za-z0-9ÁÉÍÓÚÑáéíóúñ\s_&\-]+)', line_str)
                    if fam_m:
                        current_slide['family'] = fam_m.group(1).strip()
                        
                if '<h3' in line_str or 'class="art-title"' in line_str:
                    t_m = re.search(r'<h3.*?>(.*?)</h3>', line_str)
                    if t_m:
                        current_slide['title'] = t_m.group(1).strip()
                        
                if 'class="art-description"' in line_str:
                    d_m = re.search(r'class="art-description.*?">(.*?)</p>', line_str)
                    if d_m:
                        current_slide['desc'] = d_m.group(1).strip()

    # Append last card/slide
    if in_double_column and current_card and current_card['idx_html'] and current_card['title'] and current_card['img_src']:
        slides.append(current_card)
    elif current_slide and current_slide['idx_html'] and current_slide['title'] and current_slide['img_src']:
        slides.append(current_slide)
        
    print(f"Total recovered slides sequentially: {len(slides)}")
    
    # Map back to tuple format
    tuple_slides = []
    for s in slides:
        tuple_slides.append((
            s['orig_idx_comment'],
            s['style_name_comment'],
            s['img_src'],
            s['idx_html'],
            s['title'],
            s['family'],
            s['desc']
        ))
        
    return tuple_slides

if __name__ == "__main__":
    recovered = recover()
    if len(recovered) == 48:
        print("PERFECT! Recovered all 48 slides!")
    else:
        print(f"Error: Only recovered {len(recovered)} slides.")
