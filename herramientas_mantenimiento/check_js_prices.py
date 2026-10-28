import json
import os

root = r"C:\Users\Usuario\.gemini\antigravity-ide\scratch\01_APLICACIONES_Y_WEB\GALERIA_DUDEDUART"
data_js_path = os.path.join(root, "js", "data.js")

with open(data_js_path, "r", encoding="utf-8") as f:
    content = f.read()

# Parse the JSON part
json_part = content.split("const artworkData =")[1].strip().rstrip(";")
artworks = json.loads(json_part)

for art in artworks[:10]:
    print(f"ID: {art.get('id')} | Cat: {art.get('category')} | Price: {art.get('price')}")
