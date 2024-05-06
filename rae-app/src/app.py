import json
import threading
import asyncio
import time
from typing import cast

from qreader import QReader
import depthai as dai
import webrtc_python
import msgpack
from rae_sdk.robot import Robot
from tinyrpc.protocols.msgpackrpc import (
    MSGPACKRPCProtocol,
)
from pipeline import create_pipeline
from connection import Connection


LOCALHOST = "127.0.0.1"


class RaeDemo:
    robot = None
    device: dai.Device
    qreader: QReader

    connection: Connection | None = None

    def __init__(self):
        print("Initializing rae demo")
        # self.robot = Robot()
        self.qreader = QReader()

        available_devices = dai.Device.getAllAvailableDevices()
        local_devices = list(
            filter(lambda deviceInfo: deviceInfo.name == LOCALHOST, available_devices)
        )
        if not local_devices:
            raise RuntimeError("No local devices found")

        self.device = dai.Device(local_devices[0])

        pipeline = create_pipeline(self.device)
        self.device.startPipeline(pipeline)

    def stream_data(self):
        left_camera_queue = self.device.getOutputQueue(
            name="left_cam", maxSize=4, blocking=False
        )

        while True:
            if left_camera_queue.has():
                img = left_camera_queue.get()
                message = {
                    "queue": "camera",
                    "data": img.getData().tobytes(),
                    "width": img.getWidth(),
                    "height": img.getHeight(),
                }
                data = cast(bytes, msgpack.dumps(message))

                if self.connection:
                    self.connection.broadcast(data)

    def connection_handler(self, client_id: str):
        print(f"[{client_id}] Opening connection ...")

        self.connection = Connection(client_id)

        while True:
            try:
                self.connection.accept()
            except Exception as e:
                print(e)

            time.sleep(3)

    # Read connection config from a QR code
    def read_connection_config(self):
        main_camera_queue = self.device.getOutputQueue(
            name="main_cam", maxSize=4, blocking=False
        )

        print("Reading connection config ...")

        while True:
            if main_camera_queue.has():
                img = main_camera_queue.get()

                qr_detections = self.qreader.detect(img.getCvFrame())
                if qr_detections:
                    print(qr_detections)

                decoded_contents = map(
                    lambda d: self.qreader.decode(img.getCvFrame(), d), qr_detections
                )

                for qr_content in decoded_contents:
                    print("Decoded: ", qr_content)
                    try:
                        connection_config = json.loads(qr_content)
                        if "client_id" in connection_config:
                            return connection_config
                    except Exception:
                        pass

    def run(self):
        print("Running rae demo")

        connection_config = self.read_connection_config()

        stream_thread = threading.Thread(target=self.stream_data)
        stream_thread.start()

        connection_thread = threading.Thread(
            target=lambda: self.connection_handler(connection_config["client_id"])
        )
        connection_thread.start()

        rpc = MSGPACKRPCProtocol()

        while True:
            pass


if __name__ == "__main__":
    demo = RaeDemo()
    demo.run()
