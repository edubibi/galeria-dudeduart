import os
import piexif
from PIL import Image

ASSETS_DIR = "assets"
AUTHOR = "E. Ramirez"
COPYRIGHT = "\u00a9 Eduardo Ramirez - EduArt"
ARTIST_BYTES = AUTHOR.encode("utf-8")
COPYRIGHT_BYTES = COPYRIGHT.encode("utf-8")

total = 0
errors = 0

print("Inyectando metadatos de autor en todas las imágenes JPG/JPEG...")
print(f"  Autor: {AUTHOR}")
print(f"  Copyright: {COPYRIGHT}\n")

for root, dirs, files in os.walk(ASSETS_DIR):
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext not in ('.jpg', '.jpeg'):
            continue
        
        filepath = os.path.join(root, file)
        try:
            # Load current EXIF or create fresh
            try:
                img = Image.open(filepath)
                exif_bytes = img.info.get("exif", b"")
                if exif_bytes:
                    exif_dict = piexif.load(exif_bytes)
                else:
                    exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}
            except Exception:
                exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}

            # Inject author and copyright into IFD0
            exif_dict["0th"][piexif.ImageIFD.Artist] = ARTIST_BYTES
            exif_dict["0th"][piexif.ImageIFD.Copyright] = COPYRIGHT_BYTES
            exif_dict["0th"][piexif.ImageIFD.Software] = b"EduArt Gallery"

            new_exif = piexif.dump(exif_dict)
            piexif.insert(new_exif, filepath)

            rel = os.path.relpath(filepath, ASSETS_DIR)
            print(f"  [OK] {rel}")
            total += 1

        except Exception as e:
            print(f"  [ERROR] {file}: {e}")
            errors += 1

print(f"\n{'='*50}")
print(f"Proceso completado. Imágenes firmadas: {total}  |  Errores: {errors}")
print(f"{'='*50}")
