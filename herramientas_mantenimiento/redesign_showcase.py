import re
import os

# Configuration
INPUT_FILE = "behance_showcase_completo.html"
OUTPUT_FILE = "behance_showcase_completo.html" # Overwrite to apply directly

def parse_showcase():
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
    
    # Map back to tuple format for build_new_showcase
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

def get_glow_color(family, number):
    # Soft, premium watercolor washes designed for light backgrounds
    family = family.upper()
    if "YESO" in family or "GESSOLUX" in family:
        return "rgba(212, 175, 55, 0.04)" # extremely soft golden wash
    elif "SPATULA" in family or "MATERIA" in family or "ESPATAC" in family:
        return "rgba(200, 130, 40, 0.04)" # soft terracotta/amber wash
    elif "ESTRUCTURA" in family or "CUBESSE" in family:
        if number in ["12", "13", "15"]:
            return "rgba(0, 120, 255, 0.03)" # soft cian reflection
        return "rgba(100, 80, 240, 0.03)" # soft violet reflection
    elif "ENERGÍA" in family or "NEOCIRC" in family:
        return "rgba(230, 70, 20, 0.04)" # soft orange warm halo
    elif "ATMÓSFERA" in family:
        if number in ["22"]:
            return "rgba(255, 0, 128, 0.04)" # soft cyberpunk magenta wash
        elif number in ["25"]:
            return "rgba(212, 175, 55, 0.06)" # warm candlelit Rembrandt wash
        return "rgba(100, 100, 120, 0.03)" # soft misty gray wash
    return "rgba(197, 160, 89, 0.03)" # default

def build_new_showcase(slides):
    html_start = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>UNIVERSO EDUSSE — Retrospectiva Cronológica Completa</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,300;0,400;0,600;0,700;1,400&family=Montserrat:wght@200;300;400;500;600&display=swap');

        :root {
            --bg-color: #F9F8F6; /* Premium Alabaster / French Art Paper */
            --card-bg: #111111;  /* High contrast black cards kept */
            --card-border: #222222;
            --text-color: #111111; /* Sharp dark text */
            --text-muted: #555555; /* Sophisticated gray description */
            --accent: #C5A059;    /* Eduardo's Pristine Champagne Gold */
            --accent-glow: rgba(197, 160, 89, 0.05);
            --frame-border: rgba(154, 122, 62, 0.25); /* Watermark soft bronze border color (Foto 2) */
            --paspartu-color: #ffffff; /* Pure White paspartú matboard restored */
            --width: 1400px;
        }

        body {
            background-color: #f2f1ed; /* Soft grey outer wrap for paper elevation */
            margin: 0;
            padding: 0;
            font-family: 'Montserrat', sans-serif;
            color: var(--text-color);
            display: flex;
            flex-direction: column;
            align-items: center;
            overflow-x: hidden;
        }

        /* Container designed for seamless Behance layout stitch */
        .showcase-container {
            width: var(--width);
            background-color: var(--bg-color);
            display: flex;
            flex-direction: column;
            box-shadow: 0 0 80px rgba(0,0,0,0.06);
        }

        /* Universal Slide Base */
        .slide {
            width: 100%;
            min-height: 1080px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 120px 100px;
            box-sizing: border-box;
            border-bottom: 1px solid #eae7e1;
            position: relative;
            background-color: var(--bg-color);
            overflow: hidden;
        }

        /* Ambient spotlight behind each artwork using CSS Variables */
        .slide::before {
            content: '';
            position: absolute;
            width: 850px;
            height: 850px;
            background: radial-gradient(circle, var(--glow-color, rgba(197, 160, 89, 0.04)) 0%, transparent 70%);
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 1;
            pointer-events: none;
            filter: blur(50px);
            opacity: 0.35; /* Scale down the inline glow opacity automatically to look incredibly soft on light background */
        }

        /* Outlined giant background number for high-end catalog design */
        .bg-number {
            position: absolute;
            font-family: 'Playfair Display', serif;
            font-size: 16rem; /* Sophisticated text watermark size */
            font-weight: 700;
            font-style: italic;
            color: transparent;
            -webkit-text-stroke: 1px rgba(154, 122, 62, 0.07); /* Extremely soft gold outline watermark */
            bottom: -35px;
            right: 0px;
            z-index: -1; /* Always floats safely behind the text inside relative text blocks */
            pointer-events: none;
            line-height: 1;
        }
        
        .layout-inverted .bg-number {
            left: 0px;
            right: auto;
        }

        /* COVER / PORTADA */
        .cover {
            height: 1800px;
            background: radial-gradient(circle at center, #ffffff 0%, #F9F8F6 80%);
            text-align: center;
            justify-content: flex-start;
            padding-top: 140px;
            box-sizing: border-box;
            border-bottom: 2px solid var(--accent);
        }
        
        .cover::before {
            display: none;
        }

        .cover h1 {
            font-family: 'Playfair Display', serif;
            font-size: 6.8rem;
            color: #111111; /* Sharp editorial black title like Vogue/Louvre */
            margin: 0;
            letter-spacing: -2px;
            font-weight: 700;
            text-shadow: none;
        }

        .cover h2 {
            font-family: 'Montserrat', sans-serif;
            font-size: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 16px;
            margin-top: 30px;
            color: var(--accent); /* Luxurious Gold subtitle */
            font-weight: 400;
            padding-left: 16px; /* Offset spacing */
        }

        .cover-divider {
            width: 80px;
            height: 1px;
            background: linear-gradient(to right, transparent, var(--accent), transparent);
            margin: 50px auto;
        }

        .cover p {
            font-size: 1.1rem;
            color: var(--text-muted);
            letter-spacing: 6px;
            text-transform: uppercase;
            margin: 0;
            font-weight: 400;
        }

        .red-easel-container {
            margin-top: 80px;
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
        }

        .red-easel-svg {
            width: 800px;
            height: 800px;
            transition: transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
            cursor: pointer;
        }

        .red-easel-svg:hover {
            transform: translateY(-10px) scale(1.01);
        }

        /* CHAPTER WALLS / MUROS DE EXPOSICIÓN */
        .chapter-wall {
            min-height: 900px;
            background: linear-gradient(135deg, #f7f6f3 0%, #f1efe9 100%);
            border-left: 4px solid var(--accent);
            text-align: center;
            align-items: center;
            justify-content: center;
            padding: 150px;
        }

        .chapter-wall::before {
            display: none;
        }

        .chapter-content {
            max-width: 900px;
            z-index: 2;
        }

        .chapter-number {
            font-family: 'Montserrat', sans-serif;
            font-size: 1.1rem;
            color: var(--accent);
            letter-spacing: 8px;
            text-transform: uppercase;
            display: block;
            margin-bottom: 25px;
            font-weight: 600;
        }

        .chapter-title {
            font-family: 'Playfair Display', serif;
            font-size: 4.5rem;
            color: #111111;
            margin: 0;
            font-weight: 700;
            letter-spacing: -1px;
            line-height: 1.1;
        }

        .chapter-divider {
            width: 150px;
            height: 1px;
            background: var(--accent);
            margin: 40px auto;
        }

        .chapter-desc {
            font-size: 1.4rem;
            line-height: 1.8;
            color: #444444;
            font-weight: 300;
            font-family: 'Playfair Display', serif;
            font-style: italic;
        }
        
        .chapter-cross {
            font-family: 'Montserrat', sans-serif;
            color: rgba(197, 160, 89, 0.4);
            font-size: 1.2rem;
            margin-top: 50px;
            font-weight: 200;
        }

        /* PICTURE FRAME SYSTEM (MUSEUM DESIGN ON WHITE WALLS) */
        .museum-frame {
            position: relative;
            background: var(--paspartu-color); /* Paspartú solid background under the image */
            border: 1px solid var(--frame-border); /* Solid champagne gold inner border */
            box-shadow: 0 35px 70px rgba(0, 0, 0, 0.12), 
                        0 0 0 12px var(--paspartu-color),       /* Archival Warm Linen/Ivory inner paspartú mount board */
                        0 0 0 13px var(--frame-border); /* Fine outer solid champagne gold frame lip */
            border-radius: 1px;
            overflow: hidden;
            display: inline-flex; /* Lets the container shrink-wrap exactly to the image's dimensions! */
            justify-content: center;
            align-items: center;
            transition: transform 0.4s cubic-bezier(0.25, 1, 0.5, 1);
            max-width: 100%;
            width: fit-content;
            height: fit-content;
        }
        
        .museum-frame:hover {
            transform: scale(1.015);
        }

        /* ------------------------------------------------------------- */
        /* PLANTILLA A Y B: ESQUEMA SPLIT (STANDARD / INVERTED)         */
        /* ------------------------------------------------------------- */
        .art-layout {
            display: flex;
            width: 100%;
            gap: 100px;
            align-items: center;
            z-index: 2;
        }

        .layout-inverted .art-layout {
            flex-direction: row-reverse;
        }

        .art-preview-wrapper {
            flex: 1.25;
            display: flex;
            justify-content: center;
        }

        .art-img {
            max-height: 750px; /* Standardize vertical height for all artworks */
            width: auto;
            max-width: 100%;
            display: block; /* Eliminates the default inline spacing at the bottom */
            object-fit: contain;
        }

        .art-info {
            flex: 0.75;
            display: flex;
            flex-direction: column;
            justify-content: center;
            padding-right: 20px;
            position: relative; /* Stacking context anchor for bg-number watermark */
            z-index: 1;
        }
        
        .layout-inverted .art-info {
            padding-right: 0;
            padding-left: 20px;
        }

        .art-header {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 15px;
        }

        .art-number-inline {
            font-family: 'Playfair Display', serif;
            font-size: 2.2rem;
            color: var(--accent);
            font-style: italic;
            font-weight: 600;
            margin: 0;
            line-height: 1;
        }

        .art-badge {
            padding: 4px 12px;
            border: 1px solid rgba(197, 160, 89, 0.25);
            color: var(--accent);
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 2px;
            border-radius: 2px;
            background-color: rgba(197, 160, 89, 0.04);
            font-weight: 600;
        }

        .art-title {
            font-family: 'Playfair Display', serif;
            font-size: 3rem;
            color: #111111;
            margin: 0 0 25px 0;
            line-height: 1.15;
            letter-spacing: -0.5px;
            font-weight: 700;
        }

        .divider-gold {
            width: 60px;
            height: 1px;
            background: var(--accent);
            margin-bottom: 30px;
        }

        .art-description {
            font-size: 1.15rem;
            line-height: 1.8;
            color: var(--text-muted);
            margin: 0 0 45px 0;
            font-weight: 400;
            text-align: justify;
        }

        /* Technical Grid Specs for Premium Catalog feel */
        .art-metadata-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 15px;
            border-top: 1px solid #eae7e1;
            padding-top: 30px;
        }

        .meta-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.75rem;
            letter-spacing: 1.5px;
            text-transform: uppercase;
        }

        .meta-label {
            color: #777777;
            font-weight: 400;
        }

        .meta-val {
            color: #111111;
            font-weight: 600;
        }

        /* FOOTER / CIERRE */
        .footer-slide {
            height: 900px;
            background: linear-gradient(to top, #f9f8f6 0%, #f1efe9 100%);
            text-align: center;
            justify-content: center;
            border-top: 2px solid var(--accent);
        }
        
        .footer-slide::before {
            display: none;
        }

        .footer-slide h2 {
            font-family: 'Playfair Display', serif;
            font-size: 4rem;
            color: #111111;
            margin: 0 0 20px 0;
            letter-spacing: -1px;
            font-weight: 700;
        }

        .footer-slide p {
            font-size: 1.4rem;
            color: #444444;
            max-width: 750px;
            margin: 0 auto 60px auto;
            line-height: 1.8;
            font-weight: 300;
            font-family: 'Playfair Display', serif;
            font-style: italic;
        }

        .btn {
            display: inline-block;
            padding: 18px 50px;
            border: 1px solid #111111;
            color: #111111;
            text-decoration: none;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 4px;
            transition: all 0.4s ease;
            font-size: 0.85rem;
            background: transparent;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.02);
        }

        .btn:hover {
            background-color: #111111;
            color: #ffffff;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
            transform: translateY(-2px);
        }

        /* UNFRAMED CANVAS STYLE FOR MASTER COVER */
        .unframed-canvas {
            width: 100%;
            max-width: 650px;
            box-shadow: 0 45px 95px rgba(0, 0, 0, 0.16); /* Thick, soft, realistic floating shadow */
            border-radius: 4px; /* Soft canvas-wrapped corners */
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #000000;
            z-index: 2;
            transition: transform 0.4s cubic-bezier(0.25, 1, 0.5, 1);
        }
        
        .unframed-canvas:hover {
            transform: scale(1.015);
        }
        
        .unframed-canvas img {
            width: 100%;
            height: auto;
            display: block;
        }

        /* ------------------------------------------------------------- */
        /* FULL BLEED LAYOUT                                             */
        /* ------------------------------------------------------------- */
        .layout-full-bleed {
            padding: 120px 100px;
            box-sizing: border-box;
        }

        .full-bleed-wrapper {
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center; /* Center the giant shrink-wrapped bleed frame! */
            gap: 60px;
            z-index: 2;
        }

        .full-bleed-frame {
            display: inline-flex; /* Shrink-wrap the image dimensions! */
            background: var(--paspartu-color);
            box-shadow: 0 45px 90px rgba(0, 0, 0, 0.15), 
                        0 0 0 16px var(--paspartu-color), 
                        0 0 0 17px var(--frame-border);
            max-height: 850px;
            max-width: 100%;
            width: fit-content;
            height: fit-content;
        }

        .art-img-full {
            max-height: 850px;
            width: auto;
            max-width: 100%;
            display: block;
            object-fit: contain;
        }

        .full-bleed-info {
            width: 100%;
            display: flex;
            flex-direction: column;
            position: relative; /* Stacking context anchor for bg-number watermark */
            z-index: 1;
        }

        /* ------------------------------------------------------------- */
        /* DOUBLE COLUMN GRID LAYOUT                                     */
        /* ------------------------------------------------------------- */
        .layout-double-column {
            padding: 120px 100px;
            box-sizing: border-box;
        }

        .double-column-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 100px;
            width: 100%;
            z-index: 2;
        }

        .double-column-card {
            display: flex;
            flex-direction: column;
            position: relative;
            background-color: var(--bg-color);
        }

        .double-column-card .museum-frame {
            align-self: center; /* Center the frame itself inside the left-aligned text column! */
            margin-bottom: 35px;
        }

        .double-column-card .art-img {
            max-height: 600px; /* Slightly more compact for side-by-side elegant layouts */
        }

        .double-column-card .bg-number {
            font-size: 10rem; /* Perfectly scaled down watermark for double column cards */
            bottom: -15px;
            right: 0px;
        }
    </style>
</head>
<body>

    <div class="showcase-container">

        <!-- PORTADA PRINCIPAL -->
        <div class="slide cover">
            <div>
                <h1>UNIVERSO EDUSSE</h1>
                <h2>The Archive of Creative Movements</h2>
                <div class="cover-divider"></div>
                <p>Eduardo Ramírez — Retrospective Exhibition</p>
                <div class="red-easel-container">
                    <!-- Giant sharp abstract easel in electric blue -->
                    <svg class="red-easel-svg" viewBox="0 0 500 500">
                        <!-- 3 Vertical Center Posts -->
                        <line x1="225" y1="20" x2="225" y2="480" stroke="#0052FF" stroke-width="5" stroke-linecap="round" />
                        <line x1="250" y1="20" x2="250" y2="480" stroke="#0052FF" stroke-width="5" stroke-linecap="round" />
                        <line x1="275" y1="20" x2="275" y2="480" stroke="#0052FF" stroke-width="5" stroke-linecap="round" />

                        <!-- 2 Slanted Legs -->
                        <line x1="210" y1="30" x2="60" y2="460" stroke="#0052FF" stroke-width="5.5" stroke-linecap="round" />
                        <line x1="290" y1="30" x2="440" y2="460" stroke="#0052FF" stroke-width="5.5" stroke-linecap="round" />

                        <!-- 1 Top Horizontal Bar -->
                        <line x1="130" y1="90" x2="370" y2="90" stroke="#0052FF" stroke-width="6" stroke-linecap="round" />

                        <!-- 2 Bottom Horizontal Bars -->
                        <line x1="80" y1="335" x2="420" y2="335" stroke="#0052FF" stroke-width="6" stroke-linecap="round" />
                        <line x1="70" y1="350" x2="430" y2="350" stroke="#0052FF" stroke-width="6" stroke-linecap="round" />
                    </svg>
                </div>
            </div>
        </div>
"""
    
    # Process slides using an anarchic dynamic loop
    html_slides = ""
    i = 0
    
    # Anarchic dynamic layout pattern to destroy expectations!
    layout_pattern = [
        'S', 'I', 'S', 'I',  # 0, 1, 2, 3
        'F',                 # 4
        'S', 'I',            # 5, 6
        'D',                 # 7, 8 (Double Column)
        'S', 'I', 'S', 'I',  # 9, 10, 11, 12
        'F',                 # 13
        'S', 'I',            # 14, 15
        'D',                 # 16, 17 (Double Column)
        'S', 'I', 'S', 'I',  # 18, 19, 20, 21
        'F',                 # 22
        'S', 'I',            # 23, 24
        'D',                 # 25, 26 (Double Column)
        'S', 'I', 'S', 'I',  # 27, 28, 29, 30
        'F',                 # 31
        'S', 'I',            # 32, 33
        'D',                 # 34, 35 (Double Column)
        'S', 'I', 'S', 'I',  # 36, 37, 38, 39
        'F',                 # 40
        'S', 'I',            # 41, 42
        'D',                 # 43, 44 (Double Column)
        'S', 'I', 'S'        # 45, 46, 47
    ]
    
    pattern_idx = 0
    while i < len(slides):
        current_layout = layout_pattern[pattern_idx] if pattern_idx < len(layout_pattern) else 'S'
        pattern_idx += 1
        
        idx_html = slides[i][3].strip()
        
        # Inject Transition Muros chronologically
        if idx_html == "00":
            html_slides += """
        <!-- MURO DE EXPOSICIÓN I -->
        <div class="slide chapter-wall" style="--glow-color: rgba(197, 160, 89, 0.02)">
            <div class="chapter-content">
                <span class="chapter-number">Capítulo I</span>
                <h2 class="chapter-title">Los Cimientos del Alma</h2>
                <div class="chapter-divider"></div>
                <p class="chapter-desc">Exploraciones cromáticas y figurativas iniciales. La transición desde el simbolismo poético hacia los primeros carboncillos y grabados expresionistas que forjaron la identidad visual del Universo Edusse.</p>
                <div class="chapter-cross">+ &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; +</div>
            </div>
        </div>
"""
        elif idx_html == "10":
            html_slides += """
        <!-- MURO DE EXPOSICIÓN II -->
        <div class="slide chapter-wall" style="--glow-color: rgba(100, 120, 255, 0.02)">
            <div class="chapter-content">
                <span class="chapter-number">Capítulo II</span>
                <h2 class="chapter-title">La Conquista del Volumen</h2>
                <div class="chapter-divider"></div>
                <p class="chapter-desc">La llegada de las geometrías complejas, el cubismo constructivista, los prismas de refracción de vidrio macizo y el ordenamiento matemático en estructuras fractales.</p>
                <div class="chapter-cross">+ &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; +</div>
            </div>
        </div>
"""
        elif idx_html == "26":
            html_slides += """
        <!-- MURO DE EXPOSICIÓN III -->
        <div class="slide chapter-wall" style="--glow-color: rgba(212, 175, 55, 0.02)">
            <div class="chapter-content">
                <span class="chapter-number">Capítulo III</span>
                <h2 class="chapter-title">La Revolución de la Espátula</h2>
                <div class="chapter-divider"></div>
                <p class="chapter-desc">El lienzo se vuelve tridimensional. La espátula esculpe el óleo puro creando texturas extremas, relieves táctiles y composiciones brutas inspiradas en la calma zen y la arquitectura monumental.</p>
                <div class="chapter-cross">+ &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; +</div>
            </div>
        </div>
"""
        elif idx_html == "38":
            html_slides += """
        <!-- MURO DE EXPOSICIÓN IV -->
        <div class="slide chapter-wall" style="--glow-color: rgba(255, 230, 180, 0.02)">
            <div class="chapter-content">
                <span class="chapter-number">Capítulo IV</span>
                <h2 class="chapter-title">La Trascendencia del Yeso y la Neblina</h2>
                <div class="chapter-divider"></div>
                <p class="chapter-desc">La madurez artística absoluta. Texturas agrietadas de yeso calcáreo (stucco), sutiles refracciones de prismas irisados, pigmentos de azurita mineral y la bruma introspectiva final.</p>
                <div class="chapter-cross">+ &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; +</div>
            </div>
        </div>
"""
        
        if current_layout == 'S' or current_layout == 'I':
            orig_idx_comment, style_name_comment, img_src, idx_html, title, family, desc = slides[i]
            layout_class = "layout-standard" if current_layout == 'S' else "layout-inverted"
            glow_color = get_glow_color(family, idx_html)
            
            html_slides += f"""
        <!-- {orig_idx_comment} {style_name_comment} [{layout_class.upper().replace('LAYOUT-', '')}] -->
        <div class="slide {layout_class}" style="--glow-color: {glow_color}">
            <div class="art-layout">
                <div class="art-preview-wrapper">
                    <div class="museum-frame">
                        <img src="{img_src}" class="art-img" alt="{title}">
                    </div>
                </div>
                <div class="art-info">
                    <div class="bg-number">{idx_html}</div>
                    <div class="art-header">
                        <p class="art-number-inline">{idx_html}</p>
                        <span class="art-badge">FAMILIA: {family}</span>
                    </div>
                    <h3 class="art-title">{title}</h3>
                    <div class="divider-gold"></div>
                    <p class="art-description">{desc}</p>
                    <div class="art-metadata-grid">
                        <div class="meta-item"><span class="meta-label">MOVIMIENTO</span><span class="meta-val">{family}</span></div>
                        <div class="meta-item"><span class="meta-label">TÉCNICA</span><span class="meta-val">Estilo {idx_html} &bull; Pintura Digital</span></div>
                        <div class="meta-item"><span class="meta-label">SOPORTE</span><span class="meta-val">Giclée Fine Art</span></div>
                    </div>
                </div>
            </div>
        </div>
"""
            i += 1
            
        elif current_layout == 'F':
            orig_idx_comment, style_name_comment, img_src, idx_html, title, family, desc = slides[i]
            glow_color = get_glow_color(family, idx_html)
            
            html_slides += f"""
        <!-- {orig_idx_comment} {style_name_comment} [FULL-BLEED] -->
        <div class="slide layout-full-bleed" style="--glow-color: {glow_color}">
            <div class="full-bleed-wrapper">
                <div class="museum-frame full-bleed-frame">
                    <img src="{img_src}" class="art-img-full" alt="{title}">
                </div>
                <div class="full-bleed-info">
                    <div class="bg-number">{idx_html}</div>
                    <div class="art-header" style="justify-content: center; margin-bottom: 20px;">
                        <p class="art-number-inline">{idx_html}</p>
                        <span class="art-badge">FAMILIA: {family}</span>
                    </div>
                    <h3 class="art-title" style="text-align: center; font-size: 3.5rem; margin-bottom: 30px;">{title}</h3>
                    <p class="art-description" style="text-align: center; max-width: 900px; margin: 0 auto 40px auto; font-size: 1.2rem; line-height: 1.8;">{desc}</p>
                    <div class="art-metadata-grid" style="grid-template-columns: 1fr 1fr 1fr; gap: 40px; max-width: 900px; margin: 0 auto; border-top: 1px solid #eae7e1; padding-top: 30px;">
                        <div class="meta-item"><span class="meta-label">MOVIMIENTO</span><span class="meta-val">{family}</span></div>
                        <div class="meta-item"><span class="meta-label">TÉCNICA</span><span class="meta-val">Estilo {idx_html} &bull; Pintura Digital</span></div>
                        <div class="meta-item"><span class="meta-label">SOPORTE</span><span class="meta-val">Giclée Fine Art</span></div>
                    </div>
                </div>
            </div>
        </div>
"""
            i += 1
            
        elif current_layout == 'D':
            # Pair current slide with next one
            if i + 1 < len(slides):
                s1 = slides[i]
                s2 = slides[i+1]
                glow_color = get_glow_color(s1[5], s1[3])
                
                html_slides += f"""
        <!-- DOUBLE COLUMN GROUP: {s1[3]} & {s2[3]} -->
        <!-- {s1[0]} {s1[1]} -->
        <div class="slide layout-double-column" style="--glow-color: {glow_color}">
            <div class="double-column-grid">
                <!-- Column 1 -->
                <div class="double-column-card">
                    <div class="museum-frame">
                        <img src="{s1[2]}" class="art-img" alt="{s1[4]}">
                    </div>
                    <div class="art-info" style="padding: 0;">
                        <div class="bg-number">{s1[3]}</div>
                        <div class="art-header">
                            <p class="art-number-inline">{s1[3]}</p>
                            <span class="art-badge">FAMILIA: {s1[5]}</span>
                        </div>
                        <h3 class="art-title" style="font-size: 2.2rem; margin-bottom: 15px;">{s1[4]}</h3>
                        <p class="art-description" style="font-size: 1.05rem; line-height: 1.7; margin-bottom: 30px;">{s1[6]}</p>
                        <div class="art-metadata-grid" style="padding-top: 20px;">
                            <div class="meta-item"><span class="meta-label">MOVIMIENTO</span><span class="meta-val">{s1[5]}</span></div>
                            <div class="meta-item"><span class="meta-label">TÉCNICA</span><span class="meta-val">Estilo {s1[3]} &bull; Pintura</span></div>
                        </div>
                    </div>
                </div>
                <!-- Column 2 -->
                <!-- {s2[0]} {s2[1]} -->
                <div class="double-column-card">
                    <div class="museum-frame">
                        <img src="{s2[2]}" class="art-img" alt="{s2[4]}">
                    </div>
                    <div class="art-info" style="padding: 0;">
                        <div class="bg-number">{s2[3]}</div>
                        <div class="art-header">
                            <p class="art-number-inline">{s2[3]}</p>
                            <span class="art-badge">FAMILIA: {s2[5]}</span>
                        </div>
                        <h3 class="art-title" style="font-size: 2.2rem; margin-bottom: 15px;">{s2[4]}</h3>
                        <p class="art-description" style="font-size: 1.05rem; line-height: 1.7; margin-bottom: 30px;">{s2[6]}</p>
                        <div class="art-metadata-grid" style="padding-top: 20px;">
                            <div class="meta-item"><span class="meta-label">MOVIMIENTO</span><span class="meta-val">{s2[5]}</span></div>
                            <div class="meta-item"><span class="meta-label">TÉCNICA</span><span class="meta-val">Estilo {s2[3]} &bull; Pintura</span></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
"""
                i += 2
        else:
            orig_idx_comment, style_name_comment, img_src, idx_html, title, family, desc = slides[i]
            layout_class = "layout-standard"
            glow_color = get_glow_color(family, idx_html)
            
            html_slides += f"""
        <!-- {orig_idx_comment} {style_name_comment} [FALLBACK] -->
        <div class="slide {layout_class}" style="--glow-color: {glow_color}">
            <div class="art-layout">
                <div class="art-preview-wrapper">
                    <div class="museum-frame">
                        <img src="{img_src}" class="art-img" alt="{title}">
                    </div>
                </div>
                <div class="art-info">
                    <div class="bg-number">{idx_html}</div>
                    <div class="art-header">
                        <p class="art-number-inline">{idx_html}</p>
                        <span class="art-badge">FAMILIA: {family}</span>
                    </div>
                    <h3 class="art-title">{title}</h3>
                    <div class="divider-gold"></div>
                    <p class="art-description">{desc}</p>
                    <div class="art-metadata-grid">
                        <div class="meta-item"><span class="meta-label">MOVIMIENTO</span><span class="meta-val">{family}</span></div>
                        <div class="meta-item"><span class="meta-label">TÉCNICA</span><span class="meta-val">Estilo {idx_html} &bull; Pintura Digital</span></div>
                        <div class="meta-item"><span class="meta-label">SOPORTE</span><span class="meta-val">Giclée Fine Art</span></div>
                    </div>
                </div>
            </div>
        </div>
"""
            i += 1

    html_end = """
        <!-- FINAL DE LA EXPOSICIÓN -->
        <div class="slide footer-slide">
            <div>
                <h2>EDUARDO RAMÍREZ</h2>
                <p>La imaginación abre el camino, la técnica lo vuelve arte.</p>
                <a href="https://dudeduart.es" class="btn" target="_blank">Adquirir Obra / dudeduart.es</a>
            </div>
        </div>

    </div>

</body>
</html>
"""

    full_output = html_start + html_slides + html_end
    
    print(f"Writing to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(full_output)
    print("Redesign complete! File updated successfully.")

if __name__ == "__main__":
    slides = parse_showcase()
    if len(slides) == 48:
        build_new_showcase(slides)
    else:
        print(f"ERROR: Expected 48 styles, but parsed {len(slides)}. Aborting overwrite to prevent loss.")
