import webrtc_python


class Connection:
    config: webrtc_python.WebRtcConfig
    connection: webrtc_python.WebRtc

    channels = []

    def __init__(self, client_id):
        self.config = webrtc_python.WebRtcConfig(
            client_id=client_id, signaling_url="wss://signal.cloud.luxonis.com/agent/"
        )

        self.connection = webrtc_python.WebRtc(self.config)

    def accept(self):
        connection_handle = self.connection.accept_connection(10)
        webrtc_data_channel = connection_handle.create_data_channel("track")
        self.channels.append(webrtc_data_channel)

    def broadcast(self, data: bytes):
        chunk_size = 16 * 1024 - 8  # 16KB - 8 bytes for header
        content_length = len(data)
        n_chunks = (content_length // chunk_size) + 1

        for chunk_idx in range(n_chunks):
            header = chunk_idx.to_bytes(4, "big") + n_chunks.to_bytes(4, "big")

            chunk_start_idx = chunk_idx * chunk_size
            chunk_end_idx = min((chunk_idx + 1) * chunk_size, content_length)

            chunk = data[chunk_start_idx:chunk_end_idx]
            chunk = header + chunk

            for channel in self.channels:
                channel.send(chunk)

    def receive(self):
        # TODO: Implement for multiple clients
        if not self.channels:
            return
        channel = self.channels[0]

        buffer = bytearray(1000)
        bytes_read = channel.receive(buffer)

        if bytes_read > 0:
            return buffer[:bytes_read]
