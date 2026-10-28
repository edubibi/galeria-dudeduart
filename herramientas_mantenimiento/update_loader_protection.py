import os

path = 'js/loader.js'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add watermark and overlay
content = content.replace('<div class="card-image" style="background-image: url(\'${safeUrl}\'); background-color: ${art.placeholderColor || \'#ccc\'};">\n        </div>', 
                          '<div class="card-image watermarked" style="background-image: url(\'${safeUrl}\'); background-color: ${art.placeholderColor || \'#ccc\'};">\n            <div class="artwork-overlay"></div>\n        </div>')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated loader.js with protection layers.")
