import json
import os

METADATA_FILE = "metadata.json"
PORTFOLIO_FILE = "dossier_portfolio.html"

def main():
    if not os.path.exists(METADATA_FILE):
        print("Error: metadata.json no encontrado.")
        return

    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        db = json.load(f)

    # We want to insert the transition and the B2B works at the end of the 15 standard works
    # The standard works in dossier_portfolio.html end with:
    #             <div class="page-footer">15 / 15</div>
    #         </div>
    
    if not os.path.exists(PORTFOLIO_FILE):
        print("Error: dossier_portfolio.html no encontrado.")
        return

    with open(PORTFOLIO_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove print assistant bar and adjust padding
    import re
    content = content.replace("padding-top: 100px;", "padding-top: 40px;")
    content = re.sub(r'<!-- Sticky Screen Assistant Bar -->\s*<div class="print-bar">.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class="print-bar">.*?</div>', '', content, flags=re.DOTALL)

    split_marker = '<div class="page-footer">15 / 15</div>\n        </div>'
    if split_marker not in content:
        # Try without newline
        split_marker = '<div class="page-footer">15 / 15</div></div>'
        if split_marker not in content:
            # Try with other whitespace variations
            parts = content.split('<!-- 15 -->')
            if len(parts) > 1:
                # We can rebuild from here
                sub_parts = parts[1].split('</div>')
                # rebuild split marker
                # Let's locate the page div's closing tag
                idx = parts[1].find('</div>', parts[1].find('page-footer'))
                if idx != -1:
                    pre_content = parts[0] + '<!-- 15 -->' + parts[1][:idx] + '</div>\n        </div>'
                else:
                    print("Error parsing dossier_portfolio.html")
                    return
            else:
                print("Error: No se pudo localizar el final de la obra 15 en dossier_portfolio.html.")
                return
    else:
        pre_content = content.split(split_marker)[0] + split_marker

    # Transition section pointing to B2B Magna
    transition_html = """

        <!-- PÁGINA DE TRANSICIÓN: SECCIÓN VIP B2B MAGNA -->
        <div class="page intro-page" style="justify-content: center; text-align: center; background: #111; color: #fff;">
            <div style="position: absolute; top: 10mm; bottom: 10mm; left: 10mm; right: 10mm; border: 1px solid rgba(197, 160, 89, 0.4); pointer-events: none; z-index: 10;"></div>
            <div style="position: relative; z-index: 20; padding: 0 10%; margin-top: auto; margin-bottom: auto;">
                <h2 style="color: var(--accent); border-bottom: 1px solid var(--accent); padding-bottom: 20px; font-family: var(--font-serif); font-size: 2.2rem; margin-top: 0; margin-bottom: 30px; letter-spacing: 2px;">
                    Espacios Singulares & Gran Formato
                </h2>
                <p style="font-size: 1.15rem; line-height: 1.8; color: #eee; margin-bottom: 24px; text-align: center; font-family: var(--font-sans);">
                    Para aquellos espacios que exigen una presencia monumental, disponemos de nuestra exclusiva colección <strong>B2B Magna</strong>.
                </p>
                <p style="font-size: 1.1rem; line-height: 1.8; color: #ccc; margin-bottom: 24px; text-align: center; font-family: var(--font-sans);">
                    Una selección de obras concebidas bajo estrictas ediciones limitadas y diseñadas específicamente para proyectos contract de alta gama: hoteles de lujo, vestíbulos corporativos, suites de prestigio y zonas comunes exclusivas.
                </p>
                <p style="font-size: 1.1rem; line-height: 1.8; color: #ccc; margin-bottom: 35px; text-align: center; font-family: var(--font-sans);">
                    Estas piezas destacan por su gran formato personalizable y la pureza de su acabado en calidad de museo.
                </p>
                <div style="margin: 30px 0;">
                    <a href="https://dudeduart.es/cuadroteca/index.html" target="_blank" style="display: inline-block; border: 1px solid var(--accent); color: var(--accent); padding: 14px 35px; font-family: var(--font-sans); font-weight: 700; text-decoration: none; text-transform: uppercase; font-size: 0.9rem; letter-spacing: 1.5px; border-radius: 4px; transition: all 0.3s ease;">
                        Explorar Colección Magna
                    </a>
                </div>
                <p style="font-size: 0.9rem; color: #888; margin-top: 20px; letter-spacing: 1px;">
                    A continuación, se muestra una selección exclusiva de piezas B2B Magna.
                </p>
            </div>
            <div class="page-footer" style="color: #666; border-top: 1px solid rgba(255,255,255,0.05);">Colección VIP / Gran Formato B2B</div>
        </div>
    """

    b2b_ids = [
        "b2b_magna_pianista_mineral",
        "b2b_magna_danza_de_color",
        "b2b_magna_paraiso_tropical",
        "b2b_magna_001",
        "b2b_magna_002",
        "b2b_magna_003",
        "b2b_magna_024"
    ]
    b2b_works = []
    for bid in b2b_ids:
        if bid in db:
            b2b_works.append(db[bid])
        else:
            print(f"Advertencia: No se encontró la obra VIP {bid} en metadata.json")

    b2b_pages_html = ""
    total_vip = len(b2b_works)
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
        <!-- Obra VIP {idx} -->
        <div class="page artwork-page">
            <div class="artwork-frame"><div class="artwork-frame-corners"></div></div>
            <div class="artwork-image-container">
                <img src="{src}" class="artwork-image" alt="{title}">
            </div>
            <div class="artwork-info">
                <h3 class="artwork-title">{title}</h3>
                <div class="artwork-meta">Colección Exclusiva B2B Magna | Dimensión sugerida: {size}</div>
                {desc_html}
                <p style="font-size: 0.85rem; font-weight: bold; color: var(--accent); margin-top: 10px; text-transform: uppercase; letter-spacing: 1px;">Edición Limitada — Tarifa Contract: {price} €</p>
            </div>
            <div class="page-footer">Colección Magna VIP - {idx} / {total_vip}</div>
        </div>
        """
        b2b_pages_html += page_html

    html_end = """
    </div>
</body>
</html>
    """

    with open(PORTFOLIO_FILE, "w", encoding="utf-8") as f:
        f.write(pre_content + transition_html + b2b_pages_html + html_end)

    print(f"Dossier Portfolio General actualizado con éxito: {PORTFOLIO_FILE}")

if __name__ == "__main__":
    main()
