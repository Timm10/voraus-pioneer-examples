"""Sync assets with the visualization."""

from pathlib import Path

from voraus_3d_visu import Visu

ASSETS = Path(__file__).parent.parent / "assets"


COLOR_RED = [0.8, 0.02, 0.05]
COLOR_GREEN = [0.02, 0.8, 0.05]

if __name__ == "__main__":
    visu = Visu(
        "http://voraus-3d-visu/",
        clear=True,
        identifier="scene",
        api_push=True,  # <-- sorgt für Übergabe an Port 8080
    )

    visu.add_model(
        model_path=ASSETS / "pallet/pallet.glb",
        position=[0.65, 0.10, 0.11],
        rotation=[0, 0, 0],
    )

    visu.add_model(
        model_path=ASSETS / "conveyor/conveyor.glb",
        position=[-0.95, -0.70, 0],
    )

    boxes = [
        visu.add_model(
            model_path=ASSETS / "box/box.glb",
            position=[-1.8 + i * 0.4, -0.7, 0.43],
        )
        for i in range(5)
    ]

    light_barrier = visu.add_model(
        model_path=ASSETS / "light_barrier/light_barrier.glb",
        position=[0.01, -0.70, 0.35],
        unique_material=True,
    )

    with visu.connection():
        visu.update(
            light_barrier.child("light_beam").material.color.rgb(*COLOR_GREEN),
        )

        input("Press <enter> to update the scene.")
        visu.update(
            boxes[4].position.x(-0.1),
            light_barrier.child("light_beam").material.color.rgb(*COLOR_RED),
        )
