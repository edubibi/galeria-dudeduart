import os

files = ['main.css', 'cuadroteca/style.css']

overlay_css = """
.artwork-overlay { 
    position: absolute; 
    top: 0; 
    left: 0; 
    width: 100%; 
    height: 100%; 
    z-index: 100; 
    background: url(data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7); /* Force tangibility */
    cursor: default;
}
.watermarked::after {
    content: '';
    position: absolute;
    bottom: 10px;
    right: 10px;
    width: 80px;
    height: 80px;
    background-image: url('/assets/branding/firma.png'); /* Try absolute from root first */
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    opacity: 0.4;
    z-index: 101;
    pointer-events: none;
}
"""

for file in files:
    if not os.path.exists(file): continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update the overlay definition
    import re
    content = re.sub(r'\.artwork-overlay\s*\{.*?\}', overlay_css.split('\n')[1], content, flags=re.DOTALL)
    
    # Fix paths
    if 'cuadroteca' in file:
        content = content.replace("url('/assets/branding/firma.png')", "url('../assets/branding/firma.png')")
    else:
        content = content.replace("url('/assets/branding/firma.png')", "url('assets/branding/firma.png')")

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated CSS with tangible overlays.")
