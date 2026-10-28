import os
import re

path = 'js/data.js'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the broken symbols
# The previous output showed: ' for Euro and YZ? for Gift
# But let's just replace the broken byte sequences if possible, or just the resulting strings
# Actually, I'll just use a direct replace of the known bad strings from the previous output
content = content.replace("'", "€")
content = content.replace("YZ?", "🎁")
content = content.replace("'", "€") # sometimes it shows differently

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

metadata_path = 'metadata.json'
with open(metadata_path, 'r', encoding='utf-8') as f:
    m_content = f.read()

m_content = m_content.replace("'", "€")
m_content = m_content.replace("YZ?", "🎁")

with open(metadata_path, 'w', encoding='utf-8') as f:
    f.write(m_content)

print("Fixed symbols in data.js and metadata.json")
