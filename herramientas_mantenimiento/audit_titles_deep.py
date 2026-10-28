import json
import re

with open('metadata.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

results = []
for k, v in data.items():
    if not isinstance(v, dict):
        continue
    title = v.get('title', '')
    issues = []
    
    # Check for file extensions (.jpg, .jpeg, .png, etc.)
    if re.search(r'\.(jpe?g|png|webp|gif)', title, re.I):
        issues.append('has_extension')
        
    # Check for long numbers / timestamps
    if re.search(r'\d{6,}', title):
        issues.append('has_timestamp_or_long_num')
        
    # Check for underscores
    if '_' in title:
        issues.append('has_underscore')
        
    # Check for raw codes like 01Exp Neocirc 005
    if re.match(r'^\d{2}[a-zA-Z]+', title):
        issues.append('raw_code_prefix')
        
    # Check for trailing numbers/digits like 001, 005
    if re.search(r'\b\d{3,}\b', title):
        issues.append('number_code')

    if issues:
        results.append((k, title, issues, v.get('category', '')))

print(f"Total obras encontradas con anomalías en título: {len(results)}")
for k, title, issues, cat in results:
    print(f"[{cat}] ID: {k} | TÍTULO: '{title}' | MOTIVO: {','.join(issues)}")
