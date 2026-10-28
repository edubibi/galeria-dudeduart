import os
import re

path = 'memorandum.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the premature closing divs after neo-lumina
# Look for the sequence that closes the container
content = content.replace('    </div>\n\n    </div>\n    <a href="#indice" class="back-to-top">&uarr; Volver al índice</a>', '    <a href="#indice" class="back-to-top">&uarr; Volver al índice</a>')

# Clean up the end of the file to have proper nesting
# The new styles 36 and 37 should be inside the container
# Current structure: ... 715: </div> (card) \n 717: </div> (container?) ...
# We'll just remove extra </div> until it's balanced.

# Let's do a more robust fix:
# 1. Remove all </div> tags between neo-lumina (715) and lineart (719)
content = re.sub(r'</div>\s*</div>\s*<a href="#indice" class="back-to-top">&uarr; Volver al índice</a>', '</div>', content)

# 2. Fix the Euro and Accents
content = content.replace('19,99â‚¬', '19,99€')
content = content.replace('í“leo', 'Óleo')

# 3. Ensure the main container is closed once at the end
# We'll remove all closing divs at the very end and add one
content = re.sub(r'</div>\s*</div>\s*</div>\s*<footer>', '</div>\n\n    <footer>', content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Balanced divs and fixed encoding in memorandum.html")
