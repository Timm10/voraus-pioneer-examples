import sys
import os
import time
from voraus_3d_visu import Visu
from simulate_process.simulation_runner import Simulation

# Pfad zu shared_models hinzufügen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../shared_models')))

from simulate_process.simulation_runner import Simulation
from voraus_robot_arm import VorausIndustrialRobotArm
from voraus_robot_arm import CartesianPose, JointPose

from gripper import Gripper
from box import Box
from pallet import Pallet
from conveyor import Conveyor

# Starte die Simulation
simulation = Simulation(
    frequency=50,
    visualization=Visu("http://voraus-3d-visu/", clear_all=True)
)
robot = VorausIndustrialRobotArm("voraus-core", port=48401)

gripper = Gripper()
box = Box(position=CartesianPose(x=0.6, y=0.0, z=0.1))
pallet = Pallet()
conveyor = Conveyor()

simulation.sleep(1.0)

# restlicher Code unverändert...


print("🔄 Greifer aktivieren (IO=1)...")
robot.set_digital_output(1, True)
simulation.sleep(0.5)

pick_pose = CartesianPose(x=0.6, y=0.0, z=0.2)
robot.move_linear(pick_pose).result()
simulation.sleep(0.5)

gripper_state = robot.get_digital_output(1)
if not gripper_state:
    print("❌ Greifer nicht aktiviert. Abbruch.")
else:
    print("✅ Greifer aktiviert. Fortsetzung...")

    robot.move_linear(CartesianPose(x=0.6, y=0.0, z=0.1)).result()
    simulation.sleep(0.5)

    robot.move_linear(pick_pose).result()
    simulation.sleep(0.5)

    place_pose = CartesianPose(x=0.2, y=0.0, z=0.2)
    robot.move_linear(place_pose).result()
    simulation.sleep(0.5)

    robot.set_digital_output(1, False)

