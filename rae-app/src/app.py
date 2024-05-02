import threading
import depthai as dai
from rae_sdk.robot import Robot
import asyncio
from tinyrpc.protocols.msgpackrpc import (
    MSGPACKRPCProtocol,
)
from pipeline import create_pipeline

LOCALHOST = "127.0.0.1"


class RaeDemo:
    robot = None
    device: dai.Device

    def __init__(self):
        print("Initializing rae demo")
        # self.robot = Robot()

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
                print("Received camera image")

    def connection_handler(self):
        pass

    def run(self):
        print("Running rae demo")

        stream_thread = threading.Thread(target=self.stream_data)
        stream_thread.start()

        while True:
            pass


if __name__ == "__main__":
    demo = RaeDemo()
    demo.run()
