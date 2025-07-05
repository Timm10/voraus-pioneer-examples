import pybullet as p
import pybullet_data
import time

# Start physics server
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Gravity
p.setGravity(0, 0, -9.81)

# Boden und Box
plane_id = p.loadURDF("plane.urdf")
box_id = p.loadURDF("cube.urdf", [0, 0, 1])

# Simuliere 5 Sekunden
for i in range(240 * 5):  # 240 Hz default
    p.stepSimulation()
    time.sleep(1./240.)

p.disconnect()
