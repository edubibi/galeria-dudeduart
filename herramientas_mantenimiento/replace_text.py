import os
import sys

filepath = r'C:\Users\Usuario\.gemini\antigravity-ide\scratch\01_APLICACIONES_Y_WEB\GALERIA_DUDEDUART\dossier_senart_FINAL.html'

print(f"Reading file: {filepath}")
try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
except Exception as e:
    print(f"Failed reading as utf-8: {e}")
    sys.exit(1)

target1 = '¿Cómo sueña la tecnología cuando es guiada por la sensibilidad y el corazón humano?'
target2 = '&#191;C&#243;mo sue&#241;a la tecnolog&#237;a cuando es guiada por la sensibilidad y el coraz&#243;n humano?'
replacement = 'La tecnología guiada por la sensibilidad y corazón humano'

found = False
if target1 in content:
    content = content.replace(target1, replacement)
    found = True
if target2 in content:
    content = content.replace(target2, replacement)
    found = True

if found:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replacement successful.")
else:
    print("Target string not found. The file might use a different HTML encoding or line breaks.")
