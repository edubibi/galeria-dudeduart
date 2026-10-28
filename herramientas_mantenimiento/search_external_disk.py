import os
import shutil

print("==================================================")
print("ESCANER DE DISCO EXTERNO J:\\portatil_edutilport1")
print("==================================================")

search_dir = r"J:\portatil_edutilport1"

if not os.path.exists(search_dir):
    print(f"Error: La ruta {search_dir} no está accesible o el disco J: no está conectado.")
    exit(1)

print(f"Iniciando escaneo profundo en: {search_dir}")

folders_found = []
code_matches = []
large_image_folders = []

ignored_dirs = ["node_modules", ".git", ".agent", "AppData", "System Volume Information", "$RECYCLE.BIN"]

for root, dirs, files in os.walk(search_dir):
    # Ignorar carpetas pesadas/sistema
    dirs[:] = [d for d in dirs if d not in ignored_dirs and not d.startswith(".")]
    
    # 1. Buscar por nombre de carpeta
    folder_name = os.path.basename(root).upper()
    if "CHIMERA" in folder_name or "CHIMERAS" in folder_name or "AVATAR" in folder_name or "NFT" in folder_name:
        folders_found.append((root, folder_name))
        print(f"[Carpeta Coincidente] {root}")

    # 2. Buscar por contenido de archivos de código
    image_count = 0
    for f in files:
        f_lower = f.lower()
        if f_lower.endswith(('.png', '.jpg', '.jpeg', '.webp')):
            image_count += 1
            
        if f_lower.endswith(('.html', '.js', '.py', '.txt')):
            path_file = os.path.join(root, f)
            try:
                # Leer muestras de código buscando palabras clave
                with open(path_file, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                
                if "Horda" in content or "Frost" in content or "Ártica" in content or "Abismo" in content:
                    code_matches.append((path_file, f))
                    print(f"[Código Encontrado] {path_file}")
            except Exception as e:
                pass
                
    # 3. Registrar carpetas con muchas imágenes
    if image_count > 100:
        large_image_folders.append((root, image_count))
        print(f"[Imágenes Masivas] {root} -> {image_count} archivos")

print("\n==================================================")
print("RESUMEN DE BÚSQUEDA EN DISCO J:")
print("==================================================")

print("\n--- 📂 CARPETAS COINCIDENTES ENCONTRADAS ---")
if folders_found:
    for path, name in folders_found:
        print(f"- {name}: {path}")
else:
    print("Ninguna carpeta con nombre coincidente.")

print("\n--- 💻 ARCHIVOS DE CÓDIGO CON PARÁMETROS ENCONTRADOS ---")
if code_matches:
    for path, name in code_matches:
        print(f"- {name}: {path}")
else:
    print("Ningún código con coincidencia de texto.")

print("\n--- 🖼️ COLECCIONES DE IMÁGENES GRANDES ---")
if large_image_folders:
    large_image_folders.sort(key=lambda x: x[1], reverse=True)
    for path, count in large_image_folders:
        print(f"- {path}: {count} imágenes")
else:
    print("Ninguna carpeta con más de 100 imágenes.")

print("\n==================================================")
print("ESCANEADO FINALIZADO")
print("==================================================")
