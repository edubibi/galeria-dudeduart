import os
import re

path = 'js/data.js'
backup_path = 'js/data.js.ultimate_bak'

# Read current content
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Save one more backup just in case
with open(backup_path, 'w', encoding='utf-8') as f:
    f.write(content)

# 1. Fix the syntax error in ADMIRACION
# It was: "src": "assets/35PAPERCHIN/ADMIRACI"N.png",
# We'll replace it with a safe string.
content = content.replace('"src": "assets/35PAPERCHIN/ADMIRACI"N.png"', '"src": "assets/35PAPERCHIN/ADMIRACION.png"')

# 2. Fix the category name back to "1000 SELLOS MAGICOS"
# My previous script changed it to "SELLOS MAGICOS" or "SELLOS_MAGICOS"
content = content.replace('"category": "SELLOS_MAGICOS"', '"category": "1000 SELLOS MAGICOS"')
content = content.replace('"SELLOS MAGICOS":', '"1000 SELLOS MAGICOS":')

# 3. Fix the price for the cover_book
# It was "Colección"
content = content.replace('"price": "Coleccin"', '"price": "19,99"')

# 4. Final check for common syntax errors (quotes in middle of strings)
# This is a bit complex with regex, but let's try to find potential broken lines
# A common pattern for the error is "key": "value"value",
# Let's just do a targeted fix for what we saw.

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed syntax error in ADMIRACION and restored category '1000 SELLOS MAGICOS'")
print("Restored stamp prices to 19,99")
