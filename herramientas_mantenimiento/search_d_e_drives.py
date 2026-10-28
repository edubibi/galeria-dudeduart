import os

print("==================================================")
print("ESCANER RÁPIDO DE DISCOS SECUNDARIOS D:\\ y E:\\")
print("==================================================")

search_paths = [r"D:\\", r"E:\\"]
ignored_folders = [
    "AppData", "System Volume Information", "$RECYCLE.BIN", 
    "Windows", "Program Files", "Program Files (x86)", "node_modules", ".git"
]

results = []

for start_dir in search_paths:
    if not os.path.exists(start_dir):
        continue
    print(f"\nEscaneando unidad: {start_dir}...")
    for root, dirs, files in os.walk(start_dir):
        # Evitar carpetas de sistema pesadas
        dirs[:] = [d for d in dirs if d not in ignored_folders and not d.startswith(".")]
        
        # Contar archivos de imagen
        image_count = sum(1 for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.webp')))
        
        # Filtrar por palabras clave de NFT en el nombre de la carpeta
        folder_name = os.path.basename(root).upper()
        has_keyword = "FURSONA" in folder_name or "QUANTUM" in folder_name or "CHIMERA" in folder_name or "AVATAR" in folder_name
        
        if image_count > 300 or (image_count > 0 and has_keyword):
            results.append((root, image_count))
            print(f"[Encontrado] {root} -> {image_count} archivos de imagen")

print("\n==================================================")
print("RESUMEN DE BÚSQUEDA MASIVA EN D: y E:")
print("==================================================")
if results:
    results.sort(key=lambda x: x[1], reverse=True)
    for folder, count in results:
        print(f"- {folder}: {count} imágenes")
else:
    print("No se encontraron carpetas con colecciones grandes de imágenes en D: ni E:.")
print("==================================================")
