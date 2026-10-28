import json
import re

with open('metadata.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total entries in metadata.json: {len(data)}")

ext_matches = []
timestamp_matches = []

for k, v in data.items():
    if not isinstance(v, dict):
        continue
    title = v.get('title', '')
    
    if re.search(r'\.(jpe?g|png|webp|gif)', title, re.I):
        ext_matches.append((k, title, v.get('category')))
        
    if re.search(r'\d{6,}', title):
        timestamp_matches.append((k, title, v.get('category')))

print(f"Titles with file extensions ({len(ext_matches)}):")
for k, t, c in ext_matches:
    print(f"  [{c}] {k} -> '{t}'")

print(f"\nTitles with timestamps/long numbers ({len(timestamp_matches)}):")
for k, t, c in timestamp_matches:
    print(f"  [{c}] {k} -> '{t}'")
