"""Describes a pallet simulation model."""

from pathlib import Path

from voraus_3d_visu import Visu

from voraus_simulation import StaticObject

models = Path(__file__).parent


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


if __name__ == "__main__":
    import sys
    from math import radians

    sys.path.append(str(Path(__file__).parent.parent.parent))
    from models.box.box import Box

    from voraus_simulation import Simulation

    simulation = Simulation(frequency=50, visualization=Visu("http://voraus-3d-visu/"))

    with simulation.run():
        StaticObject(glb_file=None, urdf_path=Path("plane_transparent.urdf"))
        pallet = Pallet([0.76, 0.10, 0.11], rotation=[0, 0, radians(5)])
        Box([1.24, 0.10, 0.3])

        frame = 0
        while frame < 100:
            simulation.step()
            simulation.sleep()
            frame += 1