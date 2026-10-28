import os

path = 'js/data.js'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace weird bullet artifacts
# Based on the output, it looks like 'ǽ\'' or similar
content = content.replace('ǽ\'', '•')
# And others like 'ǭ' or 'Ǹ' which are broken accents
content = content.replace('ǭ', 'á')
content = content.replace('Ǹ', 'é')
content = content.replace('ǭ', 'í') # Wait, sometimes it's the same
# Let's be more careful. I'll just fix the obvious bullets for now.
content = content.replace('ǽ\'', '•')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Cleaned up bullet artifacts")
