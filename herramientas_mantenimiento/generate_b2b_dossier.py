import json
import os
import datetime

METADATA_FILE = "metadata.json"
OUTPUT_FILE = "dossier_b2b_magna.html"

def main():
    if not os.path.exists(METADATA_FILE):
        print("Error: metadata.json no encontrado.")
        return

    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        db = json.load(f)

    # Filter for B2B Magna works
    b2b_works = []
    for key, value in db.items():
        if isinstance(value, dict) and value.get("category") == "B2B MAGNA (ACCESO EXCLUSIVO)":
            b2b_works.append(value)

    # Sort B2B works: prioritize premier pieces at the top
    def sort_b2b(item):
        iid = item.get("id", "")
        if "pianista_mineral" in iid:
            return (0, iid)
        if "danza_de_color" in iid:
            return (1, iid)
        if "paraiso_tropical" in iid:
            return (2, iid)
        if "golden_river" in iid:
            return (3, iid)
        return (4, iid)
    b2b_works.sort(key=sort_b2b)

    print(f"Encontradas {len(b2b_works)} obras de la colección B2B Magna.")

    css = """
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Lato:wght@300;400;700&display=swap');

        :root {
            --primary: #1a1a1a;
            --primary-light: #444;
            --accent: #C5A059; /* Antique Gold */
            --accent-light: rgba(197, 160, 89, 0.12);
            --font-serif: 'Playfair Display', serif;
            --font-sans: 'Lato', sans-serif;
            --page-bg: #FCFBF9; /* Warm gallery white */
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: var(--font-sans);
            color: var(--primary);
            margin: 0;
            padding: 0;
            background: #141414;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }

        .print-bar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 60px;
            background: rgba(20, 20, 20, 0.95);
            border-bottom: 1px solid rgba(197, 160, 89, 0.3);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 40px;
            z-index: 1000;
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        .print-bar-title {
            color: #fff;
            font-family: var(--font-serif);
            font-size: 1.2rem;
            letter-spacing: 1px;
        }

        .print-bar-title span {
            color: var(--accent);
            font-weight: bold;
        }

        .print-btn {
            background: linear-gradient(135deg, var(--accent) 0%, #a37f3d 100%);
            color: #111;
            border: none;
            padding: 10px 24px;
            font-family: var(--font-sans);
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.8rem;
            letter-spacing: 1px;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(197, 160, 89, 0.3);
        }

        .print-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(197, 160, 89, 0.5);
            background: linear-gradient(135deg, #d4b26f 0%, var(--accent) 100%);
        }

        .print-tip {
            color: #ccc;
            font-size: 0.8rem;
            max-width: 500px;
            text-align: right;
            line-height: 1.4;
        }

        .portfolio-container {
            padding-top: 40px;
            padding-bottom: 50px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .page {
            width: 210mm;
            height: 297mm;
            padding: 25mm 20mm;
            background: var(--page-bg);
            position: relative;
            page-break-after: always;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
            margin-bottom: 40px;
            overflow: hidden;
        }

        .cover-page {
            text-align: center;
            justify-content: center;
            background: #111;
            color: #fff;
            padding: 25mm 20mm;
            position: relative;
        }

        .cover-page::before {
            content: '';
            position: absolute;
            top: 10mm;
            bottom: 10mm;
            left: 10mm;
            right: 10mm;
            border: 1px solid var(--accent);
            pointer-events: none;
            z-index: 10;
        }

        .cover-page h1 {
            font-family: var(--font-serif);
            font-size: 2.8rem;
            color: var(--accent);
            margin: 0 0 1rem 0;
            letter-spacing: 4px;
            font-weight: 700;
        }

        .cover-page .subtitle {
            font-size: 1.1rem;
            letter-spacing: 3px;
            text-transform: uppercase;
            color: #ccc;
            margin-bottom: 2rem;
        }

        .cover-divider {
            width: 80px;
            height: 1px;
            background: var(--accent);
            margin: 0 auto 2.5rem auto;
        }

        .cover-author {
            font-size: 1.4rem;
            font-family: var(--font-serif);
            font-style: italic;
            color: #fff;
            margin-bottom: 0.5rem;
        }

        .cover-meta {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #888;
        }

        .intro-page {
            justify-content: flex-start;
            padding-top: 25mm;
        }

        .intro-page h2 {
            font-family: var(--font-serif);
            font-size: 2.2rem;
            color: var(--primary);
            border-bottom: 1px solid var(--accent);
            padding-bottom: 12px;
            margin-top: 0;
            margin-bottom: 25px;
            letter-spacing: 1px;
            font-weight: 600;
        }

        .intro-page p {
            font-size: 1.05rem;
            line-height: 1.7;
            color: var(--primary-light);
            margin-bottom: 18px;
            text-align: justify;
        }

        .intro-page strong {
            color: var(--primary);
            font-weight: 700;
        }

        .bio-footer {
            display: flex;
            align-items: center;
            gap: 30px;
            margin-top: auto;
            padding-top: 20px;
            border-top: 1px dashed rgba(0,0,0,0.1);
        }

        .portrait-container {
            width: 120px;
            height: 120px;
            border: 2px solid var(--accent);
            box-shadow: 0 8px 20px rgba(0,0,0,0.12);
            overflow: hidden;
            border-radius: 4px;
            background: #fff;
        }

        .portrait-img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .signature-text {
            font-family: var(--font-serif);
            font-size: 1.4rem;
            font-style: italic;
            color: var(--primary-light);
        }

        .signature-name {
            font-weight: 700;
            font-family: var(--font-sans);
            text-transform: uppercase;
            font-style: normal;
            letter-spacing: 2px;
            font-size: 1rem;
            color: var(--accent);
            margin-left: 10px;
            display: inline-block;
        }

        .artwork-page {
            align-items: center;
            padding: 30mm 20mm 20mm 20mm;
        }

        .artwork-frame {
            position: absolute;
            top: 10mm;
            bottom: 10mm;
            left: 10mm;
            right: 10mm;
            border: 1px solid rgba(197, 160, 89, 0.15);
            pointer-events: none;
            z-index: 10;
        }

        .artwork-frame::before, .artwork-frame::after {
            content: '';
            position: absolute;
            width: 12px;
            height: 12px;
            border-color: var(--accent);
            border-style: solid;
            pointer-events: none;
        }
        
        .artwork-frame::before {
            top: -1px;
            left: -1px;
            border-width: 2px 0 0 2px;
        }
        
        .artwork-frame::after {
            bottom: -1px;
            right: -1px;
            border-width: 0 2px 2px 0;
        }

        .artwork-frame-corners {
            position: absolute;
            width: 100%;
            height: 100%;
        }

        .artwork-frame-corners::before, .artwork-frame-corners::after {
            content: '';
            position: absolute;
            width: 12px;
            height: 12px;
            border-color: var(--accent);
            border-style: solid;
            pointer-events: none;
        }

        .artwork-frame-corners::before {
            top: -1px;
            right: -1px;
            border-width: 2px 2px 0 0;
        }

        .artwork-frame-corners::after {
            bottom: -1px;
            left: -1px;
            border-width: 0 0 2px 2px;
        }

        .artwork-image-container {
            width: 100%;
            height: 55%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 25px;
            position: relative;
            z-index: 5;
        }

        .artwork-image {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.18);
            border: 4px solid #fff;
            outline: 1px solid rgba(0,0,0,0.08);
        }

        .artwork-info {
            text-align: left;
            width: 100%;
            padding: 0 5%;
            box-sizing: border-box;
            z-index: 5;
        }

        .artwork-title {
            font-family: var(--font-serif);
            font-size: 1.7rem;
            margin: 0 0 8px 0;
            color: var(--primary);
            font-weight: 700;
            letter-spacing: 0.5px;
        }

        .artwork-meta {
            color: #666;
            font-size: 0.85rem;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            border-left: 2px solid var(--accent);
            padding-left: 10px;
            font-weight: 700;
        }

        .artwork-desc {
            font-size: 0.95rem;
            line-height: 1.6;
            color: var(--primary-light);
            margin: 0;
            text-align: justify;
        }

        .page-footer {
            width: 100%;
            text-align: center;
            font-size: 0.75rem;
            color: #aaa;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-top: 15px;
            padding-top: 10px;
            border-top: 1px solid rgba(0,0,0,0.05);
            z-index: 5;
        }

        @media screen and (max-width: 220mm) {
            body { background: #141414; padding: 10px; }
            .print-bar { position: relative; top: 0; width: 100%; margin-bottom: 20px; padding: 10px; height: auto; flex-direction: column; gap: 10px; text-align: center; }
            .print-tip { text-align: center; }
            .portfolio-container { padding-top: 0; }
            .page { width: 100%; height: auto; padding: 15mm 10mm; margin-bottom: 20px; }
            .artwork-image-container { height: auto; min-height: 250px; }
            .artwork-frame { display: none; }
        }

        @media print {
            body { background: #fff !important; color: #000 !important; }
            .print-bar { display: none !important; }
            .portfolio-container { padding: 0 !important; }
            .page { width: 210mm !important; height: 297mm !important; padding: 25mm 20mm !important; margin: 0 !important; box-shadow: none !important; page-break-after: always !important; page-break-inside: avoid !important; background: var(--page-bg) !important; border: none !important; }
            .cover-page { background: #111 !important; color: #fff !important; border: none !important; }
            .cover-page::before { border: 1px solid var(--accent) !important; }
            .artwork-frame { border: 1px solid rgba(197, 160, 89, 0.25) !important; }
            .artwork-image { box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15) !important; }
        }
    """

    html_start = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Dossier B2B Magna - Eduardo Ramírez (SENSORY ARTISTIC)</title>
    <style>{css}</style>
</head>
<body>
    <div class="portfolio-container">
        <!-- PORTADA -->
        <div class="page cover-page">
            <div style="width: 170px; height: 170px; margin: -85px auto 95px auto; overflow: hidden; border: 1px solid rgba(197, 160, 89, 0.4); box-shadow: 0 10px 25px rgba(0,0,0,0.5); position: relative; z-index: 20;">
                <img src="assets/B2B_MAGNA/Trilogía Argéntea.png" style="width: 100%; height: 100%; object-fit: cover;" alt="Trilogía Argéntea">
            </div>
            <h1>COLECCIÓN B2B MAGNA</h1>
            <div class="subtitle">Formatos Monumentales & Exclusividad Contract</div>
            <div class="cover-divider"></div>
            <div class="cover-author">Eduardo Ramírez de Cartagena</div>
            <div class="cover-meta">Dossier de Presentación para Estudios de Interiorismo y Arquitectura | 2026</div>
        </div>

        <!-- INTRODUCCIÓN B2B -->
        <div class="page intro-page">
            <h2>Colección Magna B2B</h2>
            <p><strong>El arte a gran escala como respuesta a la arquitectura contemporánea de alto nivel.</strong></p>
            <p>La colección <strong>Magna B2B</strong> ha sido concebida específicamente para vestir espacios singulares: vestíbulos residenciales de gran altura, suites presidenciales en hoteles boutique, y salas de juntas de corporaciones de prestigio. Huyendo de la escala estándar, estas piezas han sido diseñadas para dialogar con espacios de proporciones monumentales.</p>
            <p>Cada una de las obras destaca por su enorme presencia visual, su riqueza cromática y su textura, generando puntos focales de gran fuerza dramática y elegancia sobria. La producción se realiza bajo demanda bajo la supervisión directa del autor, utilizando los más altos estándares de impresión Fine Art Giclée con tintas minerales sobre lienzos de lino o papeles de algodón de pureza museo.</p>
            <p><strong>Exclusividad de Edición:</strong> Las obras B2B Magna están sujetas a una política de ediciones limitadas estrictas (máximo 15 o 5 ejemplares a nivel internacional, según la pieza) e incluyen un certificado de autenticidad físico numerado y firmado por el artista.</p>

            <div class="bio-footer">
                <div class="portrait-container">
                    <img src="assets/nova_bio_eduardo.jpg" class="portrait-img" alt="Eduardo Ramírez">
                </div>
                <div class="signature-text">
                    el autor: <span class="signature-name">Eduardo Ramírez</span>
                    <div style="font-size: 0.85rem; font-family: var(--font-sans); color: var(--accent); margin-top: 5px; letter-spacing: 1px; font-weight: normal; text-transform: none;">
                        web: dudeduart.es &nbsp;|&nbsp; email: eduardoramirez@edusse.es
                    </div>
                </div>
            </div>
            <div class="page-footer">SENSORY ARTISTIC | Introducción B2B</div>
        </div>
    """

    html_pages = ""
    total_b2b = len(b2b_works)
    for idx, art in enumerate(b2b_works, 1):
        title = art.get("title", "Sin Título")
        src = art.get("src", "")
        desc = art.get("description", "Obra exclusiva de la colección Magna B2B.")
        price = art.get("price", "Consultar")
        size = art.get("size", "Consultar")

        # Clean description formatting
        desc_clean = desc.replace("â€¢", "•").replace("\t", " ").replace("\\n", "\n").replace("\r", "")
        desc_paragraphs = desc_clean.split("\n")
        desc_html = "".join(f"<p class='artwork-desc' style='margin-bottom: 8px;'>{p.strip()}</p>" for p in desc_paragraphs if p.strip())

        page_html = f"""
        <!-- Obra {idx} -->
        <div class="page artwork-page">
            <div class="artwork-frame"><div class="artwork-frame-corners"></div></div>
            <div class="artwork-image-container">
                <img src="{src}" class="artwork-image" alt="{title}">
            </div>
            <div class="artwork-info">
                <h3 class="artwork-title">{title}</h3>
                <div class="artwork-meta">Colección B2B Magna | Dimensión sugerida: {size}</div>
                {desc_html}
                <p style="font-size: 0.85rem; font-weight: bold; color: var(--accent); margin-top: 10px; text-transform: uppercase; letter-spacing: 1px;">Edición Limitada — Tarifa Contract: {price} €</p>
            </div>
            <div class="page-footer">{idx} / {total_b2b}</div>
        </div>
        """
        html_pages += page_html

    # --- PÁGINA DE TRANSICIÓN A LA GALERÍA COMPLEMENTARIA (CUADROTECA) ---
    transition_html = """
        <!-- PÁGINA DE TRANSICIÓN: OTRAS OBRAS Y GALERÍA DE ARTE -->
        <div class="page intro-page" style="justify-content: center; text-align: center; background: #1a1a1a; color: #fff;">
            <div style="position: absolute; top: 10mm; bottom: 10mm; left: 10mm; right: 10mm; border: 1px solid rgba(197, 160, 89, 0.3); pointer-events: none; z-index: 10;"></div>
            <div style="position: relative; z-index: 20; padding: 0 10%; margin-top: auto; margin-bottom: auto;">
                <h2 style="color: var(--accent); border-bottom: 1px solid var(--accent); padding-bottom: 20px; font-family: var(--font-serif); font-size: 2.2rem; margin-top: 0; margin-bottom: 30px; letter-spacing: 2px;">
                    Catálogo de Estilos & Galería de Arte
                </h2>
                <p style="font-size: 1.15rem; line-height: 1.8; color: #eee; margin-bottom: 24px; text-align: center; font-family: var(--font-sans);">
                    Además de nuestra colección de gran formato <strong>B2B Magna</strong>, disponemos de una galería digital interactiva con una amplia variedad de obras, formatos y estilos artísticos desarrollados por el autor.
                </p>
                <p style="font-size: 1.1rem; line-height: 1.8; color: #ccc; margin-bottom: 24px; text-align: center; font-family: var(--font-sans);">
                    Estas colecciones versátiles y adaptables son ideales para vestir espacios complementarios (despachos, pasillos, salas secundarias o habitaciones de hotel), aportando coherencia visual y elegancia a todo el proyecto decorativo.
                </p>
                <p style="font-size: 1.1rem; line-height: 1.8; color: #ccc; margin-bottom: 35px; text-align: center; font-family: var(--font-sans);">
                    Puede explorar todo nuestro catálogo de estilos y colecciones interactuando directamente en:
                </p>
                <div style="margin: 30px 0;">
                    <a href="https://dudeduart.es/cuadroteca/index.html" target="_blank" style="display: inline-block; background: linear-gradient(135deg, var(--accent) 0%, #a37f3d 100%); color: #111; padding: 14px 35px; font-family: var(--font-sans); font-weight: 700; text-decoration: none; text-transform: uppercase; font-size: 0.9rem; letter-spacing: 1.5px; border-radius: 4px; box-shadow: 0 4px 15px rgba(197, 160, 89, 0.4); transition: all 0.3s ease;">
                        Explorar Galería (dudeduart.es)
                    </a>
                </div>
                <p style="font-size: 0.9rem; color: #888; margin-top: 20px; letter-spacing: 1px;">
                    A continuación, mostramos una selección representativa de estilos para espacios complementarios.
                </p>
            </div>
            <div class="page-footer" style="color: #666; border-top: 1px solid rgba(255,255,255,0.05);">Colecciones Complementarias / Cuadroteca</div>
        </div>
    """
    html_pages += transition_html

    # --- OBRAS COMPLEMENTARIAS ---
    standard_ids = ["01exp_neocirc_017", "02cubesse_stilo_001", "08boracarbon_004", "manhattan"]
    standard_works = []
    for sid in standard_ids:
        if sid in db:
            standard_works.append(db[sid])
        else:
            print(f"Advertencia: No se encontró la obra complementaria {sid} en metadata.json")

    total_std = len(standard_works)
    for idx, art in enumerate(standard_works, 1):
        title = art.get("title", "Sin Título")
        src = art.get("src", "")
        desc = art.get("description", "Obra complementaria de la colección.")
        price = art.get("price", "Consultar")
        size = art.get("size", "Consultar")
        category = art.get("category", "Colección General")

        # Clean description formatting
        desc_clean = desc.replace("â€¢", "•").replace("\t", " ").replace("\\n", "\n").replace("\r", "")
        desc_paragraphs = desc_clean.split("\n")
        desc_html = "".join(f"<p class='artwork-desc' style='margin-bottom: 8px;'>{p.strip()}</p>" for p in desc_paragraphs if p.strip())

        page_html = f"""
        <!-- Obra Complementaria {idx} -->
        <div class="page artwork-page">
            <div class="artwork-frame"><div class="artwork-frame-corners"></div></div>
            <div class="artwork-image-container">
                <img src="{src}" class="artwork-image" alt="{title}">
            </div>
            <div class="artwork-info">
                <h3 class="artwork-title">{title}</h3>
                <div class="artwork-meta">Colección Complementaria / Cuadroteca | Estilo: {category}</div>
                {desc_html}
                <p style="font-size: 0.85rem; font-weight: bold; color: var(--accent); margin-top: 10px; text-transform: uppercase; letter-spacing: 1px;">Colección General — Tarifa Contract: {price} €</p>
            </div>
            <div class="page-footer">Colección Complementaria - {idx} / {total_std}</div>
        </div>
        """
        html_pages += page_html

    html_end = """
    </div>
</body>
</html>
    """

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_start + html_pages + html_end)

    print(f"Dossier B2B Magna generado con éxito: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
