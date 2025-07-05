"""Contains a light barrier simulation model."""

from pathlib import Path

from voraus_3d_visu import Visu

from voraus_simulation import Pose, StaticObject, transforms

models = Path(__file__).parent


class LightBarrier(StaticObject):
    """Defines a light barrier simulation model."""

    def __init__(self, position: list[float], rotation: list[float] | None = None) -> None:
        """Initializes a light barrier simulation model.

        Args:
            position: The initial position of the light barrier.
            rotation: The initial rotation of the light barrier. Defaults to None.
        """
        glb_path = models / "light_barrier.glb"
        urdf_path = models / "light_barrier.urdf"
        super().__init__(glb_path, urdf_path, position, rotation)

        width = 0.4
        height = 0.05

        pose = self.get_pose()
        self.point_a = transforms.multiply(pose, Pose(position=[0, -width / 2, height], orientation=[0, 0, 0, 1]))
        self.point_b = transforms.multiply(pose, Pose(position=[0, +width / 2, height], orientation=[0, 0, 0, 1]))

    def is_clear(self) -> bool:
        """Checks if the light barrier is clear.

        Returns:
            bool: True, if clear, False if intercepted.
        """
        intersections = self.ray_test(self.point_a.position, self.point_b.position)
        if intersections and (intersections[0].object_unique_id == -1):
            return True
        return False


if __name__ == "__main__":
    import sys
    from math import radians

    sys.path.append(str(Path(__file__).parent.parent.parent))

    from models.box.box import Box
    from models.conveyor.conveyor import Conveyor

    from voraus_simulation import Simulation

    simulation = Simulation(frequency=50, visualization=Visu("http://voraus-3d-visu/"))

    with simulation.run():
        conveyor = Conveyor([0, 1.2, 0], rotation=[0, 0, radians(20)], velocity=0.5)
        conveyor_pose = conveyor.get_pose()

        lb1_pose_local = Pose(position=[-0.95, 0, 0.35], orientation=[0, 0, 0, 1])
        lb1_pose = transforms.multiply(conveyor_pose, lb1_pose_local)
        lb1 = LightBarrier(lb1_pose.position, rotation=[0, 0, radians(20)])

        lb2_pose_local = Pose(position=[0.95, 0, 0.35], orientation=[0, 0, 0, 1])
        lb2_pose = transforms.multiply(conveyor_pose, lb2_pose_local)
        lb2 = LightBarrier(lb2_pose.position, rotation=[0, 0, radians(20)])

        box = Box([-0.1, 1.2, 0.43])

        input("Press <enter> to start the example.")
        direction = -1
        while True:
            if not lb1.is_clear() and direction == -1:
                direction = 1
                input("Press <enter> to continue.")
            elif not lb2.is_clear() and direction == 1:
                direction = -1
                break

            conveyor.update(enable=True, velocity=0.5 * direction)

            simulation.step()
            conveyor.reset_pose()
            simulation.sleep()