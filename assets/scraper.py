import json, os
from datetime import datetime

# Simuliert das Finden von Kleidung
def fetch_items():
    return [
        {"brand": "Gucci", "name": "Monogram Jacket", "price": 120, "resell": 350},
        {"brand": "Nike", "name": "Vintage Hoodie", "price": 35, "resell": 95}
    ]

def update():
    if os.path.exists('assets/data.json'):
        with open('assets/data.json', 'r') as f:
            items = json.load(f)
    else: items = []

    new_drops = fetch_items()
    for drop in new_drops:
        if not any(i['name'] == drop['name'] for i in items):
            drop['id'] = str(len(items) + 1)
            drop['foundAt'] = datetime.now().isoformat()
            drop['imageUrl'] = "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=500"
            items.insert(0, drop)

    with open('assets/data.json', 'w') as f:
        json.dump(items[:50], f, indent=2)

if __name__ == "__main__":
    update()
