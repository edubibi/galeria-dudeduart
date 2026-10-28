import os
import re

path = 'js/data.js'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

fixed_lines = []
in_string = False
current_string_key = None

for line in lines:
    # This is a bit complex to do line by line because a string might span multiple lines
    # Let's try a different approach: read the whole file and use regex to find the problematic values.
    pass

# Second approach: Read whole file
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# We look for "key": "Value that starts but doesn't end on the same line"
# We'll use a regex that finds the key and then the starting quote, 
# then consumes everything until the closing quote + comma/brace.
# If there are newlines in between, we replace them with \n.

def fix_multi_line_strings(match):
    key = match.group(1)
    value = match.group(2)
    # Replace literal newlines with \n
    fixed_value = value.replace('\n', '\\n').replace('\r', '')
    return f'"{key}": "{fixed_value}"'

# This regex looks for "key": "value" where value might contain newlines
# It uses a non-greedy match for the content between quotes, but we need to be careful
# not to match across multiple keys.
# Most of these are in "description": "..."
content = re.sub(r'"(\w+)":\s*"(.*?)"(?=\s*[,}\n])', fix_multi_line_strings, content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed multi-line strings in data.js")
