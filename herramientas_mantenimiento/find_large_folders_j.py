import os

print("==================================================")
print("ESCANEANDO DISCO J EN BUSCA DE CARPETAS CON MUCHOS ARCHIVOS")
print("==================================================")

search_dir = r"J:\portatil_edutilport1"

if not os.path.exists(search_dir):
    print(f"Error: La ruta {search_dir} no está accesible.")
    exit(1)

results = []

ignored_dirs = ["node_modules", ".git", ".agent", "AppData", "System Volume Information", "$RECYCLE.BIN"]

for root, dirs, files in os.walk(search_dir):
    # Evitar carpetas del sistema
    dirs[:] = [d for d in dirs if d not in ignored_dirs and not d.startswith(".")]
    
    file_count = len(files)
    if file_count > 50:
        results.append((root, file_count))
        print(f"[Directorio] {root} -> {file_count} archivos")

print("\n==================================================")
print("RESUMEN DE BÚSQUEDA DE CARPETAS MASIVAS EN J:")
print("==================================================")
if results:
    results.sort(key=lambda x: x[1], reverse=True)
    for folder, count in results:
        print(f"- {folder}: {count} archivos")
else:
    print("No se encontraron carpetas con más de 50 archivos.")
print("==================================================")
