import os

print("==================================================")
print("BUSCANDO IMÁGENES EN UNIDADES C:, D: y E:")
print("==================================================")

search_paths = [r"C:\Users\Usuario", r"D:\\", r"E:\\"]
ignored_folders = [
    "AppData", ".gemini", ".git", ".agent", "node_modules", 
    "Windows", "$RECYCLE.BIN", "System Volume Information"
]

results = []

for start_dir in search_paths:
    if not os.path.exists(start_dir):
        continue
    print(f"\nEscaneando unidad/ruta: {start_dir} (esquivando archivos de sistema)...")
    for root, dirs, files in os.walk(start_dir):
        # Evitar carpetas del sistema
        dirs[:] = [d for d in dirs if d not in ignored_folders and not d.startswith(".")]
        
        # Filtrar por nombre de carpeta con palabras clave de NFTs
        folder_name = os.path.basename(root).upper()
        has_keyword = "FURSONA" in folder_name or "QUANTUM" in folder_name or "LAGTRIX" in folder_name
        
        # Contar imágenes
        image_count = sum(1 for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')))
        
        if image_count > 150 or (image_count > 0 and has_keyword):
            results.append((root, image_count))
            print(f"[Encontrado] {root} -> {image_count} imágenes")

print("\n==================================================")
print("RESUMEN DE BÚSQUEDA MULTI-UNIDAD:")
print("==================================================")
if results:
    results.sort(key=lambda x: x[1], reverse=True)
    for folder, count in results:
        print(f"- {folder}: {count} imágenes")
else:
    print("No se encontraron carpetas con colecciones de imágenes en C:, D: ni E:.")
print("==================================================")
