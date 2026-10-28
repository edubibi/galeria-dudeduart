import os

path = 'memorandum.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix missing closing div for neo-lumina
content = content.replace('<a href="#indice" class="back-to-top">&uarr; Volver al índice</a>\n          <div class="style-card" id="lineart">', '<a href="#indice" class="back-to-top">&uarr; Volver al índice</a>\n        </div>\n\n        <div class="style-card" id="lineart">')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed missing closing div in memorandum.html")
