import os

path = 'index.html'
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Inject protection to the hardcoded NFT images in index.html
    # They look like <img src="..."> 
    # I'll wrap them in a protected container
    import re
    def wrap_img(match):
        img_tag = match.group(0)
        if 'artwork-overlay' in img_tag: return img_tag
        return f'<div class="artwork-container watermarked"><div class="artwork-overlay"></div>{img_tag}</div>'
    
    content = re.sub(r'<img src="assets/.*?\.png".*?>', wrap_img, content)
    content = re.sub(r'<img src="assets/.*?\.jpg".*?>', wrap_img, content)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Protected hardcoded images in index.html")
