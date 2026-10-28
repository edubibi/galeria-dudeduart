import os

path = 'cuadroteca/script.js'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update createCard
old_code = "imgWrapper.className = 'art-image-wrapper';"
new_code = "imgWrapper.className = 'art-image-wrapper watermarked';\n    const overlay = document.createElement('div');\n    overlay.className = 'artwork-overlay';\n    imgWrapper.appendChild(overlay);"
content = content.replace(old_code, new_code)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated script.js with protection.")
