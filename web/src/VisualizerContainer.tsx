import { DepthAIMessageType, VisualizerContext } from "depthai-visualizer";
import { useCallback } from "react";

export function VisualizerContainer(props: { children: React.ReactNode }) {
  const messageHandler = useCallback((message: DepthAIMessageType) => {
    const now = new Date();
    const receiveTime = {
      sec: Math.floor(now.getTime() / 1000),
      nsec: now.getTime() % 1000,
    };

    if (message.type === DepthAIMessageType.ImgFrame) {
      if (
        message.category === "camera" ||
        message.category === "depth" ||
        message.category === "mono"
      ) {
        const topicByCategory = {
          camera: "/cam/color",
          depth: "/cam/depth",
          mono: "/cam/mono",
        };
        const encodingByCategory = {
          camera: "nv12",
          depth: "mono16",
          mono: "mono8",
        };

        const topic = topicByCategory[message.category];
        const encoding = encodingByCategory[message.category];

        const deserializedMessage = {
          timestamp: receiveTime,
          frame_id: "camera",
          width: message.width,
          height: message.height,
          encoding,
          step: message.width * 2,
          data: message.data,
        };

        return [
          {
            topic,
            receiveTime,
            message: deserializedMessage,
            sizeInBytes: 0,
            schemaName: "foxglove.RawImage",
          },
        ];
      } else {
        console.debug("Received unknown message category:", message.category);
        return [];
      }
    }

    return [];
  }, []);

  return (
    <VisualizerContext messageHandler={messageHandler}>
      {props.children}
    </VisualizerContext>
  );
}
