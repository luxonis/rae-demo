import depthai as dai


def create_pipeline(device: dai.Device):
    pipeline = dai.Pipeline()

    rgb = pipeline.create(dai.node.ColorCamera)
    rgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
    rgb.setFps(30)

    xRgbOut = pipeline.create(dai.node.XLinkOut)
    xRgbOut.setStreamName("rgb")

    rgb.preview.link(xRgbOut.input)

    return pipeline
