import webrtc_python


class Connection:
    config: webrtc_python.WebRTCConfig
    connection: webrtc_python.WebRTC

    channels = []

    def __init__(self, client_id):
        self.config = webrtc_python.WebRTCConfig(
            client_id=client_id, signaling_url="wss://signal.cloud.luxonis.com/agent/"
        )

        self.connection = webrtc_python.WebRTC(self.config)

    def accept(self):
        self.connection.accept_connection(10)
        webrtc_data_channel = self.connection.create_data_channel("track")
        self.channels.append(webrtc_data_channel)

    def broadcast(self, data: bytes):
        content_length = len(data)
        chunk_idx = 0
        n_chunks = (content_length // (2**14 - 2)) + 1

        while chunk_idx < n_chunks:
            header = chunk_idx.to_bytes(4, "big") + n_chunks.to_bytes(4, "big")

            chunk_start_idx = chunk_idx * 2**14
            chunk_end_idx = min((chunk_idx + 1) * 2**14, content_length)

            chunk = data[chunk_start_idx:chunk_end_idx]
            chunk = header + chunk

            for channel in self.channels:
                channel.send(chunk)
