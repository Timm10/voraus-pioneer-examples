"""Contains a light barrier simulation model."""

from pathlib import Path

from voraus_simulation import DynamicObject, Pose, transforms

models = Path(__file__).parents[2] / "assets/light_barrier"

COLOR_RED = [0.8, 0.02, 0.05]
COLOR_GREEN = [0.02, 0.8, 0.05]


class LightBarrier(DynamicObject):
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

    def get_visu_data(self) -> list:
        """Returns the visualization data for the light barrier beam.

        Returns:
            The update for the beam color.
        """
        color = COLOR_GREEN if self.is_clear() else COLOR_RED
        return [
            self.visu_object.child("light_beam").material.color.rgb(*color),
        ]
