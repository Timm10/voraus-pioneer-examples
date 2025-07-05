"""Contains a conveyor simulation model."""

from pathlib import Path

from voraus_simulation import DynamicObject

models = Path(__file__).parents[2] / "assets/conveyor"


class Conveyor(DynamicObject):
    """Describes a conveyor simulation model."""

    def __init__(self, position: list[float], rotation: list[float], velocity: float) -> None:
        """Initializes a conveyor simulation model.

        Args:
            position: The initial position.
            rotation: The initial rotation.
            velocity: The default velocity.
        """
        glb_path = models / "conveyor.glb"
        urdf_path = models / "conveyor.urdf"
        super().__init__(glb_path, urdf_path, position, rotation)

        self.velocity = velocity

    def update(self, enable: bool, velocity: float | None = None) -> None:
        """Updates the state of the conveyor.

        Args:
            enable: True if conveyor is enabled, else false.
            velocity: The velocity in m/s, uses default velocity if None. Defaults to None.
        """
        velocity = self.velocity if velocity is None else velocity
        if enable:
            self.set_velocity(linear_velocity=[velocity, 0, 0], use_local=True)
        else:
            self.set_velocity(linear_velocity=[0, 0, 0])

    def get_visu_data(self) -> list:
        """Do not update conveyor position of visual model."""
        return []
