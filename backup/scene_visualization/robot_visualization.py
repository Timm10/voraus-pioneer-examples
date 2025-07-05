"""Syncs the robot position with the voraus.core."""

import os
import time

from asyncua.sync import Client
from voraus_3d_visu import Visu

VORAUS_CORE_URL = os.getenv("VORAUS_CORE_URL", default="http://voraus-core")
ROBOT_MODEL_URL = f"{VORAUS_CORE_URL}/robots/VORAUS_INDUSTRIAL_ROBOT/VORAUS_INDUSTRIAL_ROBOT.glb"


if __name__ == "__main__":
    visu = Visu("http://voraus-3d-visu/")
    client = Client("opc.tcp://voraus-core:48401/")

    with visu.connection(), client:
        robot = visu.add_model(model_url=ROBOT_MODEL_URL, position=[0, 0, 0])
        joint_positions_node = client.get_node("ns=1;i=100111")

        while True:
            (joint_positions,) = client.read_values([joint_positions_node])

            visu.update(
                robot.child("CS0").rotation.z(joint_positions[0]),
                robot.child("CS1").rotation.z(joint_positions[1]),
                robot.child("CS2").rotation.z(joint_positions[2]),
                robot.child("CS3").rotation.z(joint_positions[3]),
                robot.child("CS4").rotation.z(joint_positions[4]),
                robot.child("CS5").rotation.z(joint_positions[5]),
            )

            time.sleep(0.01)
