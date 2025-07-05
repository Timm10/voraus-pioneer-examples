"""Moves the robot."""

from math import radians

from voraus_robot_arm import CartesianPose, JointPose, VorausIndustrialRobotArm

HOME = JointPose(0, -1.57, 1.57, -1.57, -1.57, 0)
POSE1 = CartesianPose(0.5, 0, 0.2, -radians(180), 0, radians(35))

if __name__ == "__main__":
    robot = VorausIndustrialRobotArm()
    with robot.connect("voraus-core", port=48401):
        robot.activate()

        robot.move_ptp(HOME)
        robot.move_ptp_relative(JointPose(j1=-1.57, j2=-0.3)).result()

        input("Press <enter> to move the robot again.")
        robot.move_linear(POSE1).result()
