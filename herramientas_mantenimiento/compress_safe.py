import os
from PIL import Image

assets_dir = "c:/Users/Usuario/.gemini/antigravity-ide/scratch/01_APLICACIONES_Y_WEB/GALERIA_DUDEDUART/assets"

def compress_image_safe(file_path):
    orig_size = os.path.getsize(file_path)
    if orig_size < 100 * 1024: # Skip files already smaller than 100 KB
        return False
        
    try:
        with Image.open(file_path) as img:
            # 1. Resize to max 1000px (making it extremely light "super pluma"!)
            w, h = img.size
            max_dim = 1000
            if max(w, h) > max_dim:
                img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
                
            # 2. Process based on format
            ext = os.path.splitext(file_path)[1].lower()
            
            if ext in ('.jpg', '.jpeg'):
                # Compress JPG
                img.save(file_path, format="JPEG", quality=75, optimize=True, progressive=True)
                
            elif ext == '.webp':
                # Compress WebP
                img.save(file_path, format="WebP", quality=75)
                
            elif ext == '.png':
                # ALWAYS save as valid PNG but convert to 8-bit palette (PNG-8)
                # This keeps the .png extension and makes it a 100% valid standard PNG,
                # avoiding strict MIME sniffing / server blocker issues.
                img_p = img.convert('P', palette=Image.ADAPTIVE, colors=256)
                img_p.save(file_path, format="PNG", optimize=True)
            
            new_size = os.path.getsize(file_path)
            savings = orig_size - new_size
            if savings > 0:
                print(f"  [COMPRIMIDO SEGURO] {os.path.relpath(file_path, assets_dir)}:")
                print(f"    Antes: {orig_size / 1024:.1f} KB -> Ahora: {new_size / 1024:.1f} KB (Ahorro: {savings / 1024:.1f} KB / -{((orig_size-new_size)/orig_size)*100:.1f}%)")
                return True
            else:
                return False
                
    except Exception as e:
        print(f"  [ERROR] Procesando {file_path}: {e}")
        return False

def main():
    print("Iniciando compresión SEGURA de imágenes (Máximo 1000px y formatos estándar)...")
    print(f"Buscando en: {assets_dir}\n")
    
    total_processed = 0
    total_savings = 0
    
    for root, dirs, files in os.walk(assets_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                file_path = os.path.join(root, file)
                orig_size = os.path.getsize(file_path)
                if compress_image_safe(file_path):
                    total_processed += 1
                    new_size = os.path.getsize(file_path)
                    total_savings += (orig_size - new_size)
                    
    print("\n==============================================")
    print(f"Proceso finalizado. Imágenes optimizadas: {total_processed}")
    print(f"Ahorro total de espacio: {total_savings / (1024*1024):.2f} MB")
    print("==============================================")

if __name__ == "__main__":
    main()
