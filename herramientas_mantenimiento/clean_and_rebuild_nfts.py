import os
import json
import shutil
import subprocess

print("==================================================")
print("INICIANDO PROCESO AUTOMATIZADO DE LIMPIEZA DE NFTS")
print("==================================================")

# 1. Definir Rutas
gallery_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
metadata_path = os.path.join(gallery_dir, "metadata.json")

# Rutas de Scratch Spaces
scratch_ide = os.path.abspath(os.path.join(gallery_dir, "..", ".."))
scratch_browser = r"C:\Users\Usuario\.gemini\antigravity\scratch"

# Determinar carpetas 07_OTROS_PROYECTOS
otros_ide = os.path.join(scratch_ide, "07_OTROS_PROYECTOS")
otros_browser = os.path.join(scratch_browser, "07_OTROS_PROYECTOS")

print(f"Directorio de Galería IDE: {gallery_dir}")
print(f"Directorio 07_OTROS_PROYECTOS (IDE): {otros_ide}")
print(f"Directorio 07_OTROS_PROYECTOS (Navegador): {otros_browser}")

# Asegurar que existan las carpetas de destino de otros proyectos
for path in [otros_ide, otros_browser]:
    if not os.path.exists(path):
        try:
            os.makedirs(path, exist_ok=True)
            print(f"Creada carpeta destino: {path}")
        except Exception as e:
            print(f"Nota: No se pudo crear/acceder a {path}: {e}")

# 2. Limpieza de metadata.json
print("\n--- PASO 1: Limpiando metadata.json ---")
if os.path.exists(metadata_path):
    try:
        with open(metadata_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        
        original_len = len(meta)
        # Filtrar claves
        cleaned_meta = {}
        removed_keys = []
        for k, v in meta.items():
            is_nft = False
            if k.lower().startswith("00fursona_genesis"):
                is_nft = True
            elif isinstance(v, dict):
                category = v.get("category", "")
                if "FURSONA" in category.upper() or "QUANTUM" in category.upper():
                    is_nft = True
            
            if is_nft:
                removed_keys.append(k)
            else:
                cleaned_meta[k] = v
        
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(cleaned_meta, f, indent=4, ensure_ascii=False)
        
        print(f"Metadata limpiada con éxito. Claves iniciales: {original_len}, Claves finales: {len(cleaned_meta)}")
        print(f"Se eliminaron {len(removed_keys)} obras NFT de la metadata.")
    except Exception as e:
        print(f"Error procesando metadata.json: {e}")
else:
    print("WARNING: metadata.json no encontrado!")

# 3. Mover activos físicos a 07_OTROS_PROYECTOS
print("\n--- PASO 2: Trasladando archivos de Activos ---")
assets_to_move = [
    # (origen relativo a assets, subcarpeta destino en 07_OTROS_PROYECTOS)
    ("00FURSONA GENESIS", "00FURSONA GENESIS"),
    ("fursona-geminis-2-portada.png", "00FURSONA GENESIS"),
    ("quantum-samples", "QUANTUM_DEITIES"),
    ("quantum-deities-banner.png", "QUANTUM_DEITIES"),
    ("quantum-deities-portada.png", "QUANTUM_DEITIES"),
    ("vortex-samples", "QUANTUM_DEITIES"),
    ("vortex-portada.jpg", "QUANTUM_DEITIES")
]

assets_dir = os.path.join(gallery_dir, "assets")

for item, dest_sub in assets_to_move:
    src_path = os.path.join(assets_dir, item)
    if os.path.exists(src_path):
        # Mover a ambos destinos 07_OTROS_PROYECTOS por seguridad
        moved = False
        for parent_dest in [otros_ide, otros_browser]:
            dest_dir = os.path.join(parent_dest, dest_sub)
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, os.path.basename(item))
            
            # Si ya existe en destino, borrarlo antes
            if os.path.exists(dest_path):
                if os.path.isdir(dest_path):
                    shutil.rmtree(dest_path)
                else:
                    os.remove(dest_path)
            
            try:
                if os.path.isdir(src_path):
                    shutil.copytree(src_path, dest_path)
                else:
                    shutil.copy2(src_path, dest_path)
                print(f"Copiado activo '{item}' a {dest_path}")
                moved = True
            except Exception as e:
                print(f"Error copiando '{item}' a {dest_dir}: {e}")
        
        # Eliminar del original de la galería una vez copiado
        if moved:
            try:
                if os.path.isdir(src_path):
                    shutil.rmtree(src_path)
                else:
                    os.remove(src_path)
                print(f"Eliminado activo original '{item}' de la galería.")
            except Exception as e:
                print(f"Error eliminando original '{item}': {e}")
    else:
        print(f"Nota: Activo '{item}' no encontrado en assets/ (quizás ya trasladado).")

# 4. Eliminar páginas HTML de la Galería
print("\n--- PASO 3: Eliminando páginas HTML obsoletas ---")
html_files = ["fursona-genesis.html", "quantum-deities.html"]
for hf in html_files:
    # En IDE
    ide_hf = os.path.join(gallery_dir, hf)
    if os.path.exists(ide_hf):
        try:
            os.remove(ide_hf)
            print(f"Eliminado '{hf}' de la galería del IDE.")
        except Exception as e:
            print(f"Error eliminando '{hf}' de IDE: {e}")
            
    # En Browser
    browser_hf = os.path.join(scratch_browser, "01_APLICACIONES_Y_WEB", "GALERIA_DUDEDUART", hf)
    if os.path.exists(browser_hf):
        try:
            os.remove(browser_hf)
            print(f"Eliminado '{hf}' de la galería del Navegador.")
        except Exception as e:
            print(f"Error eliminando '{hf}' del Navegador: {e}")

# 5. Ejecutar Pipeline de Compilación
print("\n--- PASO 4: Compilando base de datos e historias ---")
pipeline = [
    ["node", "herramientas_mantenimiento/rebuild_data.js"],
    ["python", "herramientas_mantenimiento/enrich_data.py"],
    ["python", "herramientas_mantenimiento/final_polish.py"],
    ["python", "herramientas_mantenimiento/generate_full_catalog.py"]
]

for cmd in pipeline:
    print(f"Ejecutando: {' '.join(cmd)}")
    try:
        res = subprocess.run(cmd, cwd=gallery_dir, capture_output=True, text=True, check=True)
        print(res.stdout)
    except FileNotFoundError:
        # Fallback to 'py' if python is not in PATH
        if cmd[0] == "python":
            fallback_cmd = ["py"] + cmd[1:]
            print(f"Probando comando alternativo: {' '.join(fallback_cmd)}")
            try:
                res = subprocess.run(fallback_cmd, cwd=gallery_dir, capture_output=True, text=True, check=True)
                print(res.stdout)
            except Exception as inner_e:
                print(f"Error con comando alternativo: {inner_e}")
        else:
            print(f"Comando no encontrado: {cmd[0]}")
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando {' '.join(cmd)}:")
        print(e.stderr)
        print("Continuando con el pipeline de todas formas...")

# 6. Sincronizar Galería Completa con la ruta del Navegador
print("\n--- PASO 5: Sincronizando cambios con el Navegador ---")
browser_gallery_dir = os.path.join(scratch_browser, "01_APLICACIONES_Y_WEB", "GALERIA_DUDEDUART")

if os.path.exists(browser_gallery_dir):
    files_to_sync = [
        "index.html",
        "galeria.html",
        "colecciones.html",
        "condiciones.html",
        "sobre-mi.html",
        "catalogo_completo.html",
        "metadata.json",
        os.path.join("js", "data.js"),
        os.path.join("js", "loader.js")
    ]
    
    for f in files_to_sync:
        src = os.path.join(gallery_dir, f)
        dst = os.path.join(browser_gallery_dir, f)
        
        if os.path.exists(src):
            try:
                # Asegurar directorio de destino
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                print(f"Sincronizado: {f} -> Navegador")
            except Exception as e:
                print(f"Error sincronizando {f}: {e}")
        else:
            print(f"Error: Archivo origen para sincronizar no encontrado: {src}")
else:
    print(f"WARNING: Directorio del Navegador {browser_gallery_dir} no existe. Sincronización omitida.")

print("\n==================================================")
print("PROCESO FINALIZADO CON ÉXITO")
print("==================================================")
