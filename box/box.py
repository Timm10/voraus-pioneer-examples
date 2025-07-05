from pathlib import Path
from voraus_3d_visu import Visu

visu = Visu("http://voraus-3d-visu/", clear_all=True)
model = Path(__file__).parent / "box.glb"

if __name__ == "__main__":
    with visu.connection():
        box = visu.add_model(model, position=[0, 0, 0])

        input("Press enter to move and rotate the box.")
        visu.update(
            box.position.x(0.3),
            box.rotation.z(1.57),
        )

        input("Press enter to make the box invisible.")
        visu.update(box.visible(False))

        input("Press enter to make the box visible.")
        visu.update(box.visible(True))

        input("Press enter to add axes helpers and parent them to the box.")
        axes_object = visu.add_axes(position=[0.3, 0, 0], rotation=[0, 0, 1.57], scale=[0.5, 0.5, 0.5])
        visu.update(axes_object.parent(box))

        input("Press enter to add another invisible box.")
        box2 = visu.add_model(model, position=[1, 0, 0], visible=False)

        input("Press enter to make the second box visible.")
        visu.update(box2.visible(True))

        input("Press enter to add a text panel")
        text_panel = visu.add_text_panel(text="Position [-1, 0, 0]", position=[-1, 0, 0])

        input("Press enter to reference the text panel to the box")
        visu.update(text_panel.parent(box), text_panel.position.xyz(0, 0, 0), text_panel.text("Box"))

        input("Press enter to hide the text panel")
        visu.update(text_panel.visible(False))

        visu.add_hash_instruction("invisible", box.visible(False), box.position.x(-5), box.scale.z(0.2))
        visu.add_hash_instruction("visible", box.visible(True))
