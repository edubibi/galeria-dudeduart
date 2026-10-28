import os
import json
import shutil
import re

METADATA_FILE = "metadata.json"
BACKUP_FILE = "metadata.backup.json"
DATA_JS_FILE = os.path.join("js", "data.js")
BACKUP_WORKSPACE_DIR = "C:/Users/Usuario/.gemini/antigravity/scratch/GALERIA_DUDEDUART"

def format_category(folder_name):
    # Default formatting: "XX FOLDERNAME" -> "XX FOLDERNAME"
    if len(folder_name) >= 2 and folder_name[:2].isdigit():
        rest = folder_name[2:].replace('_', ' ').replace('-', ' ').strip()
        # Clean up common suffixes
        if rest.lower().endswith(" stilo"):
            rest = rest[:-6]
        return f"{folder_name[:2]} {rest.upper()}"
    return folder_name.upper()

def main():
    if not os.path.exists(METADATA_FILE):
        print(f"Error: {METADATA_FILE} no encontrado en el directorio actual.")
        return

    # 1. Load existing metadata
    print("Cargando base de datos de obras (metadata.json)...")
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Backup metadata.json
    shutil.copy(METADATA_FILE, BACKUP_FILE)
    print(f"Copia de seguridad creada en {BACKUP_FILE}")

    # 2. Build folder-to-category mapping from existing items to respect established naming conventions
    folder_to_category = {}
    existing_srcs = set()
    for key, item in data.items():
        if isinstance(item, dict) and "src" in item:
            src = item["src"]
            existing_srcs.add(src)
            if "category" in item:
                # Extract folder from src (e.g. assets/47NEBULÍNICO/image.png -> 47NEBULÍNICO)
                parts = src.split('/')
                if len(parts) >= 3 and parts[0] == "assets":
                    folder_to_category[parts[1]] = item["category"]

    # 3. Scan assets/ folder
    assets_dir = "assets"
    if not os.path.exists(assets_dir):
        print(f"Error: Carpeta {assets_dir} no encontrada.")
        return

    added_items = []
    print("\nEscaneando carpetas de estilos en assets/...")
    
    for folder_name in os.listdir(assets_dir):
        folder_path = os.path.join(assets_dir, folder_name)
        if not os.path.isdir(folder_path):
            continue
            
        # Only process folders starting with two digits (e.g. "00EDUSSE", "46ESPATAC-EXTREME")
        # Exclude "00FURSONA GENESIS" (NFTs)
        if not re.match(r"^\d{2}", folder_name) or folder_name == "00FURSONA GENESIS":
            continue
            
        # Determine Category Name
        category_name = folder_to_category.get(folder_name, format_category(folder_name))
        
        # Scan for images in this folder
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                if not file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    continue
                if "_POSTER" in file_name:
                    continue
                    
                base_id = os.path.splitext(file_name)[0].lower()
                rel_path = os.path.relpath(os.path.join(root, file_name), assets_dir)
                web_src = f"assets/{rel_path.replace('\\', '/')}"
                
                # Check if this exact image file path is already registered in metadata.json
                if web_src not in existing_srcs:
                    # Clean title
                    raw_title = os.path.splitext(file_name)[0]
                    # Capitalize nicely
                    title = raw_title.replace('_', ' ').replace('-', ' ').title()
                    
                    data[base_id] = {
                        "id": base_id,
                        "title": title,
                        "category": category_name,
                        "src": web_src,
                        "description": "Nueva obra añadida recientemente.",
                        "price": "19,99",
                        "size": "Consultar"
                    }
                    added_items.append((title, category_name))
                    print(f"  [NUEVO] {title} -> Categoría: {category_name}")
                    existing_srcs.add(web_src) # Prevent duplicate addition in the same run

    # 4. Save metadata.json if changes were made
    if added_items:
        print(f"\nSe han detectado y añadido {len(added_items)} obras nuevas.")
        with open(METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
    # 5. Rebuild js/data.js
    print("Compilando js/data.js...")
    artwork_list = []
    for key, item in data.items():
        if isinstance(item, dict) and "id" in item:
            artwork_list.append(item)
    
    # Sort by category and then by ID
    artwork_list.sort(key=lambda x: (x.get("category", ""), x.get("id", "")))
    
    # Extract headers from existing data.js
    header = ""
    if os.path.exists(DATA_JS_FILE):
        with open(DATA_JS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
            parts = content.split("const artworkData =")
            if len(parts) > 0:
                header = parts[0]
    if not header:
        header = "const categoryCovers = {};\n\n"
        
    new_js_content = header + "const artworkData = " + json.dumps(artwork_list, indent=4, ensure_ascii=False) + ";"
    with open(DATA_JS_FILE, "w", encoding="utf-8") as f:
        f.write(new_js_content)
    print("¡js/data.js actualizado con éxito!")

    # 6. Sync to backup workspace if it exists
    if os.path.exists(BACKUP_WORKSPACE_DIR):
        print(f"Sincronizando archivos con el espacio de trabajo de respaldo...")
        try:
            # Copy metadata.json
            shutil.copy(METADATA_FILE, os.path.join(BACKUP_WORKSPACE_DIR, METADATA_FILE))
            # Copy js/data.js
            shutil.copy(DATA_JS_FILE, os.path.join(BACKUP_WORKSPACE_DIR, DATA_JS_FILE))
            print("¡Sincronización completada con éxito!")
        except Exception as e:
            print(f"Advertencia: No se pudo sincronizar automáticamente: {e}")

if __name__ == "__main__":
    main()
