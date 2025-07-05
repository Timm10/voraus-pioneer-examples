import time
import requests

# Basis-URL deines voraus-core Dienstes
BASE_URL = "http://voraus-core:80/api"

# Szene zurücksetzen
resp = requests.post(f"{BASE_URL}/scene/reset")
print(f"Scene reset: {resp.status_code}")

# Box erzeugen
box_payload = {
    "size": [200, 200, 200],  # 200mm Kantenlänge
    "pose": [0, 0, 100],      # Z-Höhe 100mm
}
resp = requests.post(f"{BASE_URL}/scene/add_box", json=box_payload)
print(f"Box added: {resp.status_code}")

# Szene updaten
resp = requests.post(f"{BASE_URL}/scene/update")
print(f"Scene updated: {resp.status_code}")

# Warten, damit man was sieht
for i in range(10):
    print(f"Waiting {i}...")
    time.sleep(1)

# Szene erneut updaten (optional)
resp = requests.post(f"{BASE_URL}/scene/update")
print(f"Scene updated again: {resp.status_code}")
