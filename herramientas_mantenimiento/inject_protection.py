import os

files = ['index.html', 'colecciones.html', 'memorandum.html', 'cuadroteca/index.html']

for file in files:
    if not os.path.exists(file): continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    script_path = 'js/protection.js'
    if 'cuadroteca' in file:
        script_path = '../js/protection.js'
    
    tag = f'<script src="{script_path}"></script>'
    
    if tag not in content:
        # Insert before closing body
        content = content.replace('</body>', f'    {tag}\n</body>')
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Added protection script to {file}")

print("Inclusion complete.")
