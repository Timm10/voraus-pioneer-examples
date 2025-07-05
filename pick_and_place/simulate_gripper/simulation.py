"""Contains the simulation logic, which represents the real system.."""

import sys
from math import radians
from pathlib import Path

sys.path.append(str(Path(__file__).parents[1]))


if __name__ == "__main__":
    from simulate_gripper.models import Box, Gripper, Robot
    from voraus_3d_visu import Visu
    from voraus_simulation import Simulation, StaticObject

    simulation = Simulation(frequency=50, visualization=Visu("http://voraus-3d-visu/", clear_all=True))
    robot = Robot("opc.tcp://voraus-core:48401/", [0, 0, 0.3], rotation=[0, 0, radians(-20)])

    with simulation.run(), robot.connection():
        StaticObject(glb_file=None, urdf_path=Path("plane_transparent.urdf"))

        gripper = Gripper()
        box = Box([0.6, 0.1, 0.2], rotation=[0, 0, radians(15)])

        while True:
            robot.get_robot_data()

            grasp = robot.robot_data.digital_outputs[1]
            gripper.update(robot.robot_data.world_flange_pose, grasping=grasp)

            simulation.step()
            simulation.sleep()
