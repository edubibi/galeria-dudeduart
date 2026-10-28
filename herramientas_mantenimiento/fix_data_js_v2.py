import os
import re

path = 'js/data.js'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Use regex to find "src": "assets/35PAPERCHIN/ADMIRACI...N.png"
# and fix it.
content = re.sub(r'"src":\s*"assets/35PAPERCHIN/ADMIRACI.*?N\.png"', '"src": "assets/35PAPERCHIN/ADMIRACION.png"', content)

# Ensure "category": "SELLOS_MAGICOS" becomes "category": "1000 SELLOS MAGICOS"
content = content.replace('"category": "SELLOS_MAGICOS"', '"category": "1000 SELLOS MAGICOS"')

# Fix any other potential unescaped quotes in descriptions or titles (common error)
# For example, if there is a " inside a string value like "title": "Something " Special",
# but that's harder to automate without breaking valid JSON.
# Let's focus on the one we know.

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed syntax error using regex.")
