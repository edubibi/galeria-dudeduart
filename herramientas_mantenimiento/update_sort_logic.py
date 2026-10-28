import os

path = 'cuadroteca/script.js'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make sorting logic more robust
content = content.replace("a.includes('1000 SELLOS MAGICOS')", "a.toUpperCase().includes('SELLOS')")
content = content.replace("b.includes('1000 SELLOS MAGICOS')", "b.toUpperCase().includes('SELLOS')")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated script.js sorting logic to be more robust.")
