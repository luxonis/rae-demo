import depthai as dai


def create_pipeline(device: dai.Device):
    pipeline = dai.Pipeline()
    camera_features = device.getConnectedCameraFeatures()
    left_camera_socket, right_camera_socket = None, None

    for camera in camera_features:
        if not right_camera_socket and camera.name == "right":
            right_camera_socket = camera.socket
        if not left_camera_socket and camera.name == "left":
            left_camera_socket = camera.socket

    if not (left_camera_socket and right_camera_socket):
        raise RuntimeError(
            "Both left and right cameras are required for stereo depth calculation"
        )

    left_cam = pipeline.create(dai.node.ColorCamera)
    left_cam.setInterleaved(True)
    left_cam.setBoardSocket(left_camera_socket)
    left_cam.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
    left_cam.setResolution(dai.ColorCameraProperties.SensorResolution.THE_800_P)
    left_cam.setPreviewSize(640, 480)
    left_cam.setFps(30)

    xLeftCamOut = pipeline.create(dai.node.XLinkOut)

    left_cam.preview.link(xLeftCamOut.input)

    xLeftCamOut.setStreamName("left_cam")

    return pipeline
