import os
import requests
import json

# Configuration from GitHub Secrets
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
# Use a service like 'ntfy.sh' for free phone notifications without an app
PUSH_URL = "https://ntfy.sh/your_unique_topic_12345" 

def check_vinted():
    # This is a simplified mock of the scraper logic
    # In a real scenario, you'd use a request to the Vinted API here
    drops = [
        {"brand": "Gucci", "item": "Silk Scarf", "price": "€40", "resell": "€120"},
        {"brand": "Nike", "item": "Air Max", "price": "€30", "resell": "€80"}
    ]
    return drops

def notify():
    items = check_vinted()
    for item in items:
        # 1. Logic: Filter for Brand
        if item['brand'].lower() == "gucci":
            message = f"🚨 BRAND ALERT: {item['brand']}\nItem: {item['item']}\nPrice: {item['price']}\nEst. Resell: {item['resell']}"
            
            # 2. Send to Discord
            if DISCORD_WEBHOOK:
                requests.post(DISCORD_WEBHOOK, json={"content": message})
            
            # 3. Send to Phone (via ntfy.sh - free, no login needed)
            requests.post(PUSH_URL, data=message.encode('utf-8'))

if __name__ == "__main__":
    notify()
