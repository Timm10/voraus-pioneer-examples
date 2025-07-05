# clear_scene.py
from voraus_3d_visu import Visu
import time

# Direkte Initialisierung, kein `with`
visu = Visu("http://voraus-3d-visu", clear=True, identifier="scene")

# Kurzes Warten und Update senden
time.sleep(0.5)
visu.connect()
visu.update()

print("✅ Szene wurde erfolgreich geleert.")


if __name__ == "__main__":
    visu = Visu("http://voraus-3d-visu", clear=True, identifier="scene")
    # keine weiteren Objekte hinzufügen = Szene ist leer
    print("🧹 Szene wurde geleert.")
