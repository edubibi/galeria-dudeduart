import os
import json
from PIL import Image

ASSETS_DIR = r"C:\Users\Usuario\.gemini\antigravity-ide\scratch\01_APLICACIONES_Y_WEB\GALERIA_DUDEDUART\assets\49ARTE_CIBERNETICO"
METADATA_FILE = r"C:\Users\Usuario\.gemini\antigravity-ide\scratch\01_APLICACIONES_Y_WEB\GALERIA_DUDEDUART\metadata.json"

def optimize_and_rename_images():
    print("--- 1. Optimizing and renaming images ---")
    files = os.listdir(ASSETS_DIR)
    processed_files = []
    
    for filename in files:
        if not (filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg")):
            continue
            
        old_path = os.path.join(ASSETS_DIR, filename)
        
        # Clean name (remove trailing spaces before extension)
        base, ext = os.path.splitext(filename)
        clean_base = base.strip()
        clean_filename = f"{clean_base}{ext}"
        new_path = os.path.join(ASSETS_DIR, clean_filename)
        
        if old_path != new_path:
            os.rename(old_path, new_path)
            print(f"Renamed: '{filename}' -> '{clean_filename}'")
        
        # Optimize image
        try:
            with Image.open(new_path) as img:
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if width > 1600px
                max_width = 1600
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_size = (max_width, int(img.height * ratio))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Save with optimization
                img.save(new_path, "JPEG", quality=85, optimize=True)
            print(f"Optimized: {clean_filename}")
        except Exception as e:
            print(f"Error optimizing {clean_filename}: {e}")
            
        processed_files.append(clean_filename)
        
    return processed_files

def update_metadata(processed_files):
    print("\n--- 2. Updating metadata.json ---")
    with open(METADATA_FILE, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
        
    added_count = 0
    for i, filename in enumerate(sorted(processed_files)):
        base_name, _ = os.path.splitext(filename)
        # Create an ID matching other collections pattern
        entry_id = f"49arte_cibernetico_{i+1:03d}"
        
        if entry_id not in metadata:
            metadata[entry_id] = {
                "id": entry_id,
                "title": base_name, # Use the user's file name as title
                "category": "49 ARTE CIBERNETICO",
                "src": f"assets/49ARTE_CIBERNETICO/{filename}",
                "description": f"Exploración visual del Universo EDUSSE. La pieza '{base_name}' fusiona lo cibernético con lo místico en un entorno de Arte Digital de Vanguardia.",
                "size": "Digital",
                "price": "Consultar",
                "tech_info": "Arte Digital - Universo EDUSSE (Colección Quantum & Vortex)",
                "sold": False
            }
            added_count += 1
            print(f"Added to metadata: {entry_id} -> {base_name}")
    
    if added_count > 0:
        with open(METADATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
        print(f"Successfully saved {added_count} new entries to metadata.json")
    else:
        print("No new entries added to metadata.")

if __name__ == "__main__":
    processed = optimize_and_rename_images()
    update_metadata(processed)
