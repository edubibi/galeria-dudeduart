import os
import shutil

print("==================================================")
print("INICIANDO DETALLE DE LIMPIEZA ADICIONAL Y DESANIDADO")
print("==================================================")

# Rutas
scratch_ide = r"C:\Users\Usuario\.gemini\antigravity-ide\scratch"
scratch_browser = r"C:\Users\Usuario\.gemini\antigravity\scratch"

browser_assets = os.path.join(scratch_browser, "01_APLICACIONES_Y_WEB", "GALERIA_DUDEDUART", "assets")
ide_assets = os.path.join(scratch_ide, "01_APLICACIONES_Y_WEB", "GALERIA_DUDEDUART", "assets")

otros_ide = os.path.join(scratch_ide, "07_OTROS_PROYECTOS")
otros_browser = os.path.join(scratch_browser, "07_OTROS_PROYECTOS")

print(f"Browser Assets: {browser_assets}")
print(f"Otros IDE: {otros_ide}")
print(f"Otros Browser: {otros_browser}")

# 1. Eliminar físicamente los NFT del directorio del navegador (Browser)
items_to_delete = [
    "00FURSONA GENESIS",
    "fursona-geminis-2-portada.png",
    "quantum-samples",
    "quantum-deities-banner.png",
    "quantum-deities-portada.png",
    "vortex-samples",
    "vortex-portada.jpg"
]

print("\n--- PASO 1: Eliminando NFTs del directorio del navegador (Browser) ---")
for item in items_to_delete:
    # Eliminar en Navegador
    path_browser = os.path.join(browser_assets, item)
    if os.path.exists(path_browser):
        try:
            if os.path.isdir(path_browser):
                shutil.rmtree(path_browser)
            else:
                os.remove(path_browser)
            print(f"Eliminado de assets de Navegador: {item}")
        except Exception as e:
            print(f"Error eliminando {path_browser}: {e}")
    else:
        print(f"Activo ya limpio en Navegador: {item}")

    # Eliminar en IDE (por si quedó algo)
    path_ide = os.path.join(ide_assets, item)
    if os.path.exists(path_ide):
        try:
            if os.path.isdir(path_ide):
                shutil.rmtree(path_ide)
            else:
                os.remove(path_ide)
            print(f"Eliminado de assets de IDE: {item}")
        except Exception as e:
            print(f"Error eliminando {path_ide}: {e}")

# 2. Corregir anidamientos duplicados en 07_OTROS_PROYECTOS
# Si existe otros/00FURSONA GENESIS/00FURSONA GENESIS, desanidarlo
print("\n--- PASO 2: Desanidando carpetas duplicadas en 07_OTROS_PROYECTOS ---")

for root_dest in [otros_ide, otros_browser]:
    if not os.path.exists(root_dest):
        continue
    
    # Ruta de la carpeta principal
    fursona_main = os.path.join(root_dest, "00FURSONA GENESIS")
    fursona_nested = os.path.join(fursona_main, "00FURSONA GENESIS")
    
    if os.path.exists(fursona_nested) and os.path.isdir(fursona_nested):
        print(f"Corrigiendo anidamiento duplicado en: {fursona_main}")
        
        # Mover todos los archivos de fursona_nested a fursona_main
        try:
            for f_item in os.listdir(fursona_nested):
                src_f = os.path.join(fursona_nested, f_item)
                dst_f = os.path.join(fursona_main, f_item)
                
                # Si existe en destino, borrarlo antes
                if os.path.exists(dst_f):
                    if os.path.isdir(dst_f):
                        shutil.rmtree(dst_f)
                    else:
                        os.remove(dst_f)
                
                shutil.move(src_f, dst_f)
            
            # Eliminar la carpeta anidada ahora vacía
            os.rmdir(fursona_nested)
            print(f"Desanidado con éxito para: {fursona_main}")
        except Exception as e:
            print(f"Error al desanidar en {fursona_main}: {e}")

print("\n==================================================")
print("LIMPIEZA ADICIONAL COMPLETADA CON ÉXITO")
print("==================================================")
