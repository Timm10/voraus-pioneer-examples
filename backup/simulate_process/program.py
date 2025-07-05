# pylint: disable=forgotten-debug-statement, protected-access
"""Contains the program which controls the system."""

import time
from math import radians
from threading import Thread

import numpy
from voraus_robot_arm import CartesianPose, Factor, JointPose, VorausIndustrialRobotArm, z

box_size = numpy.array([0.215, 0.331, 0.165])
box_size = box_size + 0.02

place_start = CartesianPose(0.4, -0.21, 0.07, radians(180), 0, radians(90))
place_poses = [
    place_start + CartesianPose(x * box_size[0], y * box_size[1], z * box_size[2])
    for z in range(2)
    for y in reversed(range(2))
    for x in reversed(range(2))
]


def conveyor_control(robot_arm: VorausIndustrialRobotArm) -> None:
    """The conveyor control loop."""
    dio = robot_arm._driver.dio
    while True:
        # Turn off the conveyor while the light barrier is detecting something.
        dio.set_digital_output(pin=2, value=False)
        while dio.read_digital_output(pin=3):
            time.sleep(0.01)

        time.sleep(2)

        # Turn on the conveyor while the light barrier does not detect anything
        dio.set_digital_output(pin=2, value=True)
        while not dio.read_digital_output(pin=3):
            time.sleep(0.01)


if __name__ == "__main__":
    robot = VorausIndustrialRobotArm()

    home = JointPose(0, -1.57, 1.57, -1.57, -1.57, 0)
    pre_pick = CartesianPose(-0.098, -0.705, 0.340, -radians(180), 0, -radians(180))
    pick = CartesianPose(-0.098, -0.705, 0.22, -radians(180), 0, -radians(180))

    with robot.connect("voraus-core", port=48401):
        robot.set_time_override(Factor(0.8))
        robot._driver.tool.set_offset(CartesianPose(0, 0, 0.103, 0, 0, 0))

        thread = Thread(daemon=True, target=conveyor_control, args=[robot])
        thread.start()

        robot.activate()

        count = 0
        while True:
            robot.move_ptp(home)

            # Wait for a new box
            robot.move_ptp(pre_pick).result()
            while not robot._driver.dio.read_digital_output(pin=3):
                time.sleep(0.1)

            if count == 0:
                input("Press <enter> to continue.")

            # Pick box
            robot.move_linear(pick).result()
            robot._driver.dio.set_digital_output(pin=1, value=True)
            robot.move_linear(pre_pick)

            # Place box
            place = place_poses[count]
            robot.move_ptp(place + z(0.05 + box_size[2]))
            robot.move_linear(place).result()
            robot._driver.dio.set_digital_output(pin=1, value=False)

            count += 1
