import os
import re

path = 'memorandum.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix the double back-to-top links
content = content.replace('<a href="#indice" class="back-to-top">&uarr; Volver al índice</a>\n        <a href="#indice" class="back-to-top">&uarr; Volver al índice</a>', '<a href="#indice" class="back-to-top">&uarr; Volver al índice</a>')

# 2. Fix the Euro symbol (using entity for safety)
content = content.replace('19,99?', '19,99 &euro;')
content = content.replace('19,99â‚¬', '19,99 &euro;')

# 3. Fix the closing of the container
# We need one </div> before footer to close .memo-container
if '</div>\n\n    <footer>' not in content:
    content = content.replace('    <footer>', '    </div>\n\n    <footer>')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Polished memorandum.html structure and symbols.")
