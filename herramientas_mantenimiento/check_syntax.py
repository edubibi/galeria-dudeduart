import json
import re

path = 'js/data.js'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Try to extract the JSON part of artworkData
match = re.search(r'const\s+artworkData\s*=\s*\[(.*)\];', content, re.DOTALL)
if not match:
    print("Could not find artworkData array")
    exit(1)

json_body = match.group(1)
# artworkData contains a string at the beginning: "Escribe aquí..."
# We need to skip it to parse the rest as a list of objects.
# Or better, let's try to parse the whole thing as a JS array.

# We'll replace the first string and try to parse the objects.
blocks = re.findall(r'\{(.*?)\}', json_body, re.DOTALL)
print(f"Found {len(blocks)} object blocks")

success_count = 0
for i, block in enumerate(blocks):
    try:
        # Wrap in {} and try to parse
        # Note: JS isn't strict JSON, so we might need a more lenient parser
        # but let's see if we find any obvious breaks.
        pass
    except Exception as e:
        print(f"Error in block {i}: {e}")

# Let's check for any unescaped quotes in the whole file
# A " followed by something that isn't a colon or comma or closing brace
# is suspicious if it's inside a value.
# But that's hard.

# Let's check for the "clon" work again.
# Search for any line that has more than 2 quotes but doesn't end in comma or brace.
lines = content.split('\n')
for i, line in enumerate(lines):
    if line.count('"') % 2 != 0:
        print(f"Line {i+1} has odd number of quotes: {line}")
