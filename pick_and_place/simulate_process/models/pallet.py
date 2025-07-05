"""Describes a pallet simulation model."""

from pathlib import Path

from voraus_simulation import StaticObject

models = Path(__file__).parents[2] / "assets/pallet"


class Pallet(StaticObject):
    """Defines a pallet simulation model."""

    def __init__(self, position: list[float] | None = None, rotation: list[float] | None = None) -> None:
        """Initializes a pallet simulation model.

        Args:
            position: The initial position. Defaults to None.
            rotation: The initial rotation. Defaults to None.
        """
        glb_path = models / "pallet.glb"
        urdf_path = models / "pallet.urdf"
        super().__init__(glb_path, urdf_path, position, rotation)
