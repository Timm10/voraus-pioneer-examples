import time
import voraus

# Verbindung zum lokalen voraus.core Dienst aufbauen
v = voraus.connect("localhost")

# Szene zurücksetzen
v.scene.reset()

# Einfachen Box-Slot erzeugen
box = v.scene.add_box(size=(200, 200, 200), pose=[0, 0, 100])

# Kamera einmal neu rendern lassen
v.scene.update()

# Warten um in der 3D-Visu was zu sehen
for i in range(10):
    print(f"Running... {i}")
    time.sleep(1)

# Objekt entfernen (optional)
v.scene.remove_object(box)
v.scene.update()

print("Fertig.")
