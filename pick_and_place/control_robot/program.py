from math import radians
from voraus_robot_arm import JointPose, CartesianPose, VorausIndustrialRobotArm

HOME = JointPose(0, -1.57, 1.57, -1.57, 1.57, 0)
POSE1 = CartesianPose(0.4, 0.1, 0.2, radians(180), 0, radians(10))

if __name__ == "__main__":
    robot = VorausIndustrialRobotArm()
    try:
        with robot.connect("voraus-core", port=48401):
            robot.activate()
            print("✅ Robot aktiviert")

            robot.move_ptp(HOME).result()  # ohne timeout
            print("✅ HOME erreicht")

            input("Press <Enter> to move the robot again.")
            robot.move_linear(POSE1).result()  # ebenfalls ohne timeout
            print("✅ Bewegung zu POSE1 abgeschlossen")

    except Exception as e:
        print(f"❌ Fehler während Bewegung: {e}")
