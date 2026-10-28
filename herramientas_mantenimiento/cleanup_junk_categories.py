import json
import os
import re
import sys
import shutil

# Force UTF-8 for output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

METADATA_FILE = "metadata.json"
BACKUP_FILE = "metadata.backup_limpieza.json"

def clean_artwork_title(title):
    if not title:
        return ""
    
    # Replace underscores and hyphens with spaces first
    title = title.replace("_", " ").replace("-", " ")
    
    # 1. Strip initial counting numbers (e.g., "29 ", "46_")
    # But preserve 4-digit years (like 1982, 2024)
    match = re.match(r'^(\d+)([\s\-_]*)', title)
    if match:
        digits, sep = match.groups()
        if len(digits) == 4 and (digits.startswith("19") or digits.startswith("20")):
            # Keep the year, but clean up separator
            title = digits + " " + title[len(digits) + len(sep):]
        else:
            # It's a style count or serial number, strip it
            title = title[len(digits) + len(sep):]

    # 2. Keywords/Reference names to remove case-insensitively
    keywords = [
        "EDUSSE", "CUBESSE", "NEOCIRC", "EXPNEO", "APLICC", "PLUMINK", "NEOINK", "BORACARBON",
        "FRACNEO", "OLEOCUBBO", "URBANSPHERIC", "RECTESSE", "TEREXSE", "FUZZTESS", "FUZZLINE",
        "ESPATAC", "NEBULINICO", "NEBULÍNICO", "EXTREME", "EXTREMUM", "AZURITE", "IRIS", "GESSOLUX",
        "OLONATUR", "OLENATUR", "SINNOIR", "MINIGESTPOETIC", "EXPTERICO", "PAPERCHIN", "IMPASTUS",
        "MATERDIGISSE", "MECHPASTOSSE", "SELLOS", "MAGICOS", "CUBESSEPLUS", "stilo", "ESP", "MAT", "stilo"
    ]
    
    # Remove keywords as whole words
    for kw in keywords:
        title = re.sub(r'(?i)\b' + re.escape(kw) + r'\b', '', title)
        
    # 3. Clean up formatting (multiple spaces, leading/trailing hyphens/underscores/spaces)
    title = re.sub(r'\s+', ' ', title)
    title = title.strip(" -_")
    
    # Capitalize the first letter
    if title:
        title = title[0].upper() + title[1:]
        
    return title

def cleanup():
    print(f"Loading {METADATA_FILE}...")
    try:
        with open(METADATA_FILE, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading {METADATA_FILE}: {e}")
        return

    # Create backup first
    shutil.copy(METADATA_FILE, BACKUP_FILE)
    print(f"Backup created at {BACKUP_FILE}")

    keys_to_remove = []
    cleaned_titles_count = 0

    print("Analyzing entries...")
    for key, item in data.items():
        if not isinstance(item, dict):
            continue
            
        category = item.get("category", "")
        cat_lower = category.lower()
        
        # 1. Identify junk categories
        is_junk = (
            "sample" in cat_lower or 
            "branding" in cat_lower or 
            cat_lower == "general" or 
            cat_lower == "bg" or
            not category
        )
        
        if is_junk:
            print(f"Marking junk category for removal: {key} (Category: {category})")
            keys_to_remove.append(key)
            continue
            
        # 2. Clean titles of valid artworks
        original_title = item.get("title", "")
        cleaned_title = clean_artwork_title(original_title)
        
        if cleaned_title != original_title:
            print(f"Cleaning title for [{key}]: '{original_title}' -> '{cleaned_title}'")
            item["title"] = cleaned_title
            cleaned_titles_count += 1

    # Remove junk keys
    if keys_to_remove:
        print(f"Removing {len(keys_to_remove)} junk entries...")
        for key in keys_to_remove:
            if key in data:
                del data[key]
                
    # Save the cleaned metadata
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print(f"\nCLEANUP SUCCESS:")
    print(f"- Junk entries removed: {len(keys_to_remove)}")
    print(f"- Artwork titles cleaned: {cleaned_titles_count}")

if __name__ == "__main__":
    cleanup()
