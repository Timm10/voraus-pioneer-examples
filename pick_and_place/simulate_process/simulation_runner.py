"""Contains the simulation logic, which represents the real system.."""

import sys
from pathlib import Path

from voraus_3d_visu import Visu
from voraus_simulation import Simulation, StaticObject

sys.path.append(str(Path(__file__).parents[1]))


if __name__ == "__main__":
    from simulate_process.models import Box, Conveyor, Gripper, LightBarrier, Pallet, Robot

    simulation = Simulation(frequency=50, visualization=Visu("http://voraus-3d-visu/", clear_all=True))
    robot = Robot("opc.tcp://voraus-core:48401/", [0, 0, 0.3])

    with simulation.run(), robot.connection():
        StaticObject(glb_file=None, urdf_path=Path("plane_transparent.urdf"))
        gripper = Gripper()
        conveyor = Conveyor([-0.95, -0.70, 0], rotation=[0, 0, 0], velocity=0.5)
        pallet = Pallet(position=[0.65, 0.10, 0.11])
        light_barrier = LightBarrier([0.01, -0.70, 0.35])

        for i in range(5):
            Box([-1.8 + i * 0.4, -0.7, 0.43])

        for pin in [1, 2]:
            robot.set_digital_output(pin, False)

        prev_light_barrier_state = None

        while True:
            robot.get_robot_data()
            dio1, dio2 = robot.robot_data.digital_outputs[:2]

            # Update the gripper simulation: Grasp if digital output 1 is set.
            gripper.update(robot.robot_data.world_flange_pose, grasping=dio1)

            # Update the conveyor simulation: Set velocity if digital output 2 is set.
            conveyor.update(dio2, velocity=0.5)

            # Get the state of the light barrier simulation and set it to digital output 3.
            obj_detected = not light_barrier.is_clear()
            if obj_detected != prev_light_barrier_state:
                robot.set_digital_output(3, obj_detected)
                prev_light_barrier_state = obj_detected

            simulation.step()
            conveyor.reset_pose()
            simulation.sleep()
