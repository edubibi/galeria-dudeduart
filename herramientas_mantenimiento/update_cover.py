import os

path = 'js/data.js'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update the cover image for MATERDIGISSE
# It currently has whatever was first alphabetically
# We want: assets/39MATERDIGISSE/dogo grand.png
old_pattern = r'"39 MATERDIGISSE": "assets/39MATERDIGISSE/.*?",'
new_line = '"39 MATERDIGISSE": "assets/39MATERDIGISSE/dogo grand.png",'

import re
content = re.sub(old_pattern, new_line, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated MATERDIGISSE cover to Dogo Grand.")
