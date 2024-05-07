import depthai as dai


def create_pipeline(device: dai.Device):
    pipeline = dai.Pipeline()

    rgb = pipeline.create(dai.node.ColorCamera)
    rgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
    rgb.setPreviewSize(640, 480)
    rgb.setFps(30)

    encoder = pipeline.create(dai.node.VideoEncoder)
    encoder.setDefaultProfilePreset(30, dai.VideoEncoderProperties.Profile.H264_MAIN)
    encoder.setQuality(100)
    encoder.input.setBlocking(False)
    encoder.input.setQueueSize(1)
    rgb.video.link(encoder.input)

    xRgbOut = pipeline.create(dai.node.XLinkOut)
    xRgbOut.setStreamName("rgb")
    rgb.preview.link(xRgbOut.input)

    xEncoderOut = pipeline.create(dai.node.XLinkOut)
    xEncoderOut.setStreamName("h264")
    encoder.bitstream.link(xEncoderOut.input)

    return pipeline
