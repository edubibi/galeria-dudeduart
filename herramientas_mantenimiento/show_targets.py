import json

with open('metadata.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

targets = [
    '07neoink_stilo_004', '07neoink_stilo_014', 'abuelo_paseando',
    'barco_transatlantico_impastus', 'canada_alberta_port1', 'canada_alberta_port2',
    'canada_alberta_streets', '14terexse_002', '01exp_neocirc_005.jpg_202607201144',
    'concentric_circular_strokes_past…_202607201149',
    'monasterio_del_escorial_oil_pain…_202607201524',
    'flock_of_sheep_in_meadow_202607211214',
    'kasar_ouled_soltane__tunez.jpeg_202607211222'
]

for t in targets:
    if t in data:
        item = data[t]
        print(f"ID: {t} | Title: {item.get('title')} | Cat: {item.get('category')} | Price: {item.get('price')} | Src: {item.get('src')}")
