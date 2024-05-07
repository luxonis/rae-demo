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
        connection_handle = self.connection.accept_connection(10)
        webrtc_data_channel = connection_handle.create_data_channel("track")
        self.channels.append(webrtc_data_channel)

    def broadcast(self, data: bytes):
        chunk_size = 16 * 1024 - 8  # 16KB - 8 bytes for header
        content_length = len(data)
        chunk_idx = 0
        n_chunks = (content_length // chunk_size) + 1

        while chunk_idx < n_chunks:
            header = chunk_idx.to_bytes(4, "big") + n_chunks.to_bytes(4, "big")

            chunk_start_idx = chunk_idx * chunk_size
            chunk_end_idx = min((chunk_idx + 1) * chunk_size, content_length)

            chunk = data[chunk_start_idx:chunk_end_idx]
            chunk = header + chunk

            for channel in self.channels:
                channel.send(chunk)
