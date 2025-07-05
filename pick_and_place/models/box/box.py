"""Contains a box simulation model."""

from pathlib import Path

from voraus_3d_visu import Visu

from voraus_simulation import DynamicObject

models = Path(__file__).parent


class Box(DynamicObject):
    """Defines a box simulation model."""

    def __init__(self, position: list[float] | None = None, rotation: list[float] | None = None) -> None:
        """Initializes a box simulation model.

        Args:
            position: The initial position of the box. Defaults to None.
            rotation:  The initial rotation of the box. Defaults to None.
        """
        glb_path = models / "box.glb"
        urdf_path = models / "box.urdf"
        super().__init__(glb_path, urdf_path, position, rotation)


if __name__ == "__main__":
    from voraus_simulation import Simulation, StaticObject

    simulation = Simulation(frequency=50, visualization=Visu("http://voraus-3d-visu/"))

    with simulation.run():
        StaticObject(glb_file=None, urdf_path=Path("plane_transparent.urdf"))

        for i in range(10):
            Box([-0.1, -0.2, 0.43 + i * 0.20])
        box = Box([2.0, -0.25, 0.43])

        frame = 0
        while True:
            if frame == 100:
                input("Press <enter> to apply force.")
            elif 100 <= frame < 125:
                box.apply_external_force([-80, 0, 0])
            elif frame == 125:
                input("Press <enter> to continue.")
            elif frame > 300:
                break

            simulation.step()
            simulation.sleep()
            frame += 1