import json
from collections import Counter

METADATA_FILE = "metadata.json"

with open(METADATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Count works by category
category_counter = Counter()
price_counter = Counter()

for key, item in data.items():
    if isinstance(item, dict) and "category" in item:
        category_counter[item["category"]] += 1
        price_counter[item.get("price", "19,99")] += 1

print("ARTWORK COUNT BY CATEGORY:")
print("--------------------------")
for cat, count in sorted(category_counter.items()):
    print(f" - {cat}: {count} works")

print("\nCURRENT PRICES IN METADATA.JSON:")
print("--------------------------------")
for price, count in price_counter.items():
    print(f" - {price} EUR: {count} works")
