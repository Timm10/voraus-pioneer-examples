"""Contains a conveyor simulation model."""

from pathlib import Path

from voraus_3d_visu import Visu

from voraus_simulation import DynamicObject

models = Path(__file__).parent


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


if __name__ == "__main__":
    import sys

    sys.path.append(str(Path(__file__).parent.parent.parent))

    from models.box.box import Box

    from voraus_simulation import Simulation

    simulation = Simulation(frequency=50, visualization=Visu("http://voraus-3d-visu/"))

    with simulation.run():
        conveyor = Conveyor([0.95, 0.7, 0], rotation=[0, 0, 0], velocity=0.5)
        box = Box([0.1, 0.7, 0.43])

        frame = 0
        while True:
            if frame == 100:
                input("Press <enter> to start the conveyor.")
            elif 100 <= frame < 200:
                conveyor.update(True, velocity=+0.5)
            if frame == 200:
                input("Press <enter> to stop the conveyor.")
            elif 200 < frame < 250:
                conveyor.update(False)
            elif frame == 250:
                input("Press <enter> to start the conveyor in opposite direction.")
            elif 250 < frame < 300:
                conveyor.update(True, velocity=-1.0)
            elif frame > 350:
                break

            simulation.step()
            conveyor.reset_pose()
            simulation.sleep()
            frame += 1