import time
import requests

# Achtung: Port 8077 für 3D-Visu REST API
BASE_URL = "http://voraus-3d-visu:80/api"

# Szene zurücksetzen
resp = requests.post(f"{BASE_URL}/scene/reset")
print(f"Scene reset: {resp.status_code}")

# Box erzeugen (sichtbar in Visu)
box_payload = {
    "size": [200, 200, 200],   # Würfelgröße in mm
    "pose": [0, 0, 100]        # Position (X, Y, Z)
}
resp = requests.post(f"{BASE_URL}/scene/add_box", json=box_payload)
print(f"Box added: {resp.status_code}")

# Szene aktualisieren, damit Box erscheint
resp = requests.post(f"{BASE_URL}/scene/update")
print(f"Scene updated: {resp.status_code}")

# Kurze Wartezeit, damit Bild stabil bleibt
for i in range(10):
    print(f"Waiting {i}...")
    time.sleep(1)

# Optional: Box wieder entfernen
resp = requests.post(f"{BASE_URL}/scene/remove_object", json={"id": 1})
print(f"Box removed: {resp.status_code}")
resp = requests.post(f"{BASE_URL}/scene/update")
print(f"Scene updated again: {resp.status_code}")

print("Fertig.")
