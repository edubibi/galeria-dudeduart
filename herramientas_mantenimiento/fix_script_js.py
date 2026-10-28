import os

path = 'cuadroteca/script.js'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'data.forEach(item => {' in line:
        new_lines.append(line)
        new_lines.append('        if (typeof item !== "object" || item === null) return;\n')
    else:
        new_lines.append(line)

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Fixed script.js crash by adding object check.")
