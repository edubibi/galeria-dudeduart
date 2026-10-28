import os
import re

path = 'js/data.js'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix encoding issues in known words
content = content.replace('Mǭgicos', 'Mágicos')
content = content.replace('mstica', 'mística')
content = content.replace('Coleccin', 'Colección')
content = content.replace('descripcin', 'descripción')
content = content.replace('precisin', 'precisión')
content = content.replace('tǸcnica', 'técnica')

# Ensure category is 1000 SELLOS MAGICOS
content = content.replace('"category": "SELLOS_MAGICOS"', '"category": "1000 SELLOS MAGICOS"')

# I'll set price to "Consultar" by default for stamps if the user said 19.99 is wrong,
# but actually I'll wait for their answer.
# For now I'll just fix the encoding.

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Cleaned up encoding issues in data.js")
