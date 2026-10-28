"""
embed_images_dossier.py
Convierte dossier_portfolio.html y dossier_portfolio_online.html en archivos autocontenidos
con todas las imágenes incrustadas en base64 y optimizadas para la web.
"""
import base64
import os
import re
import io
from pathlib import Path

# Rutas
BASE_DIR = Path(__file__).parent.parent

def compile_dossier(input_filename, output_filename):
    input_path = BASE_DIR / input_filename
    output_path = BASE_DIR / output_filename

    if not input_path.exists():
        print(f"Saltando {input_filename}: No existe.")
        return

    print(f"\nLeyendo: {input_path}")
    html = input_path.read_text(encoding="utf-8")

    # Encontrar todos los src de imágenes
    img_refs = re.findall(r'src=["\']([^"\']+\.(png|jpg|jpeg|gif|webp|svg))["\']', html, re.IGNORECASE)

    print(f"Encontradas {len(img_refs)} referencias a imágenes")
    replaced = 0
    errors = 0

    for src, ext in img_refs:
        # Saltar URLs externas
        if src.startswith("http://") or src.startswith("https://") or src.startswith("data:"):
            continue
        
        # Resolver ruta relativa desde la carpeta del HTML
        img_path = BASE_DIR / src.replace("/", os.sep)
        
        if img_path.exists():
            ext_lower = ext.lower()
            if ext_lower in ("png", "jpg", "jpeg", "webp"):
                try:
                    from PIL import Image
                    img = Image.open(img_path)
                    
                    # Convertir a RGB (eliminar alpha para guardar en JPEG)
                    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        alpha_channel = img.convert('RGBA').split()[3]
                        background.paste(img, mask=alpha_channel)
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Ajustar resolución a un máximo de 1600px
                    MAX_SIZE = 1600
                    if max(img.size) > MAX_SIZE:
                        img.thumbnail((MAX_SIZE, MAX_SIZE), Image.Resampling.LANCZOS)
                    
                    # Comprimir como JPEG al 80%
                    buffer = io.BytesIO()
                    img.save(buffer, format="JPEG", quality=80, optimize=True)
                    img_bytes = buffer.getvalue()
                    mime = "image/jpeg"
                    b64 = base64.b64encode(img_bytes).decode("utf-8")
                except Exception as pil_err:
                    print(f"  Advertencia: Error optimizando {src} con PIL ({pil_err}). Se usará original.")
                    img_bytes = img_path.read_bytes()
                    b64 = base64.b64encode(img_bytes).decode("utf-8")
                    mime_map = {
                        "jpg": "image/jpeg", "jpeg": "image/jpeg", 
                        "png": "image/png", "gif": "image/gif", 
                        "webp": "image/webp", "svg": "image/svg+xml"
                    }
                    mime = mime_map.get(ext_lower, "image/jpeg")
            else:
                img_bytes = img_path.read_bytes()
                b64 = base64.b64encode(img_bytes).decode("utf-8")
                mime_map = {
                    "jpg": "image/jpeg", "jpeg": "image/jpeg", 
                    "png": "image/png", "gif": "image/gif", 
                    "webp": "image/webp", "svg": "image/svg+xml"
                }
                mime = mime_map.get(ext_lower, "image/jpeg")
                
            data_uri = f"data:{mime};base64,{b64}"
            
            # Reemplazar en el HTML
            old_src_escaped = re.escape(src)
            html = re.sub(
                r'(src=["\'])' + old_src_escaped + r'(["\'])',
                r'\g<1>' + data_uri + r'\g<2>',
                html
            )
            replaced += 1
        else:
            print(f"  ERROR - NO ENCONTRADA: {img_path}")
            errors += 1

    # Hardcodear colores CSS para garantizar renderizado correcto
    html = html.replace("var(--accent-light)", "rgba(197, 160, 89, 0.12)")
    html = html.replace("var(--accent)", "#C5A059")
    html = html.replace("var(--primary-light)", "#444")
    html = html.replace("var(--primary)", "#1a1a1a")
    html = html.replace("var(--page-bg)", "#FCFBF9")
    html = html.replace("var(--font-serif)", "'Playfair Display', serif")
    html = html.replace("var(--font-sans)", "'Lato', sans-serif")

    # Guardar resultado
    output_path.write_text(html, encoding="utf-8")
    size_mb = output_path.stat().st_size / (1024*1024)

    print(f"DOSSIER GENERADO: {output_filename} ({size_mb:.1f} MB)")
    print(f"   Imágenes incrustadas: {replaced} | Errores: {errors}")

if __name__ == "__main__":
    # 1. Compilar versión para imprimir PDF (con barra de herramientas)
    compile_dossier("dossier_portfolio.html", "dossier_senart_FINAL.html")
    
    # 2. Compilar versión para ver Online (limpia sin barra)
    compile_dossier("dossier_portfolio_online.html", "dossier_senart_ONLINE.html")

    # 3. Compilar versión en Inglés para imprimir PDF (con barra de herramientas)
    compile_dossier("dossier_portfolio_en.html", "dossier_senart_en_FINAL.html")

    # 4. Compilar versión en Inglés para ver Online (limpia sin barra)
    compile_dossier("dossier_portfolio_en_online.html", "dossier_senart_en_ONLINE.html")
    
    print("\n¡Compilación terminada para todas las versiones!")
