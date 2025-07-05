# pylint: disable=protected-access
"""Contains the program which controls the robot."""

from math import radians

from voraus_robot_arm import CartesianPose, JointPose, VorausIndustrialRobotArm, y

home = JointPose(0, -1.57, 1.57, -1.57, -1.57, 0)
scan = JointPose(radians(-63), radians(-131), radians(80), radians(-80), radians(-60), radians(-10))
pre_pick = CartesianPose(0.5, 0.3, -0.05, -radians(180), 0, -radians(180))
pick = CartesianPose(0.5, 0.3, -0.128, -radians(180), 0, -radians(180))
offset = -0.6


if __name__ == "__main__":
    robot = VorausIndustrialRobotArm()

    with robot.connect("voraus-core", port=48401):
        robot._driver.tool.set_offset(CartesianPose(0, 0, 0.103, 0, 0, 0))
        robot.activate()

        input("Press <enter> to pick the box.")
        robot.move_ptp(pre_pick)
        robot.move_linear(pick).result()
        robot._driver.dio.set_digital_output(pin=2, value=True)

        robot.move_ptp(scan)

        input("Press <enter> to place the box.")
        robot.move_ptp(pre_pick + y(offset)).result()
        robot._driver.dio.set_digital_output(pin=2, value=False)
