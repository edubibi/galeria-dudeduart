import os

path = 'js/data.js'
metadata_path = 'metadata.json'

def update_offer_text():
    # 1. Update data.js
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_offer = "Pack 5: 3,90€"
    new_offer = "Pack 5 (diferentes o iguales): 3,90€"
    content = content.replace(old_offer, new_offer)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    # 2. Update metadata.json
    with open(metadata_path, 'r', encoding='utf-8') as f:
        m_content = f.read()
    
    m_content = m_content.replace(old_offer, new_offer)
    
    with open(metadata_path, 'w', encoding='utf-8') as f:
        f.write(m_content)

    print("Updated offer text with '(diferentes o iguales)'")

if __name__ == "__main__":
    update_offer_text()
