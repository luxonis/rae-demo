import webrtc_python
import threading


class Connection:
    config: webrtc_python.WebRtcConfig
    connection: webrtc_python.WebRtc

    connection_lock = threading.Lock()

    clients = []

    def __init__(self, client_id):
        self.config = webrtc_python.WebRtcConfig(
            client_id=client_id, signaling_url="wss://signal.cloud.luxonis.com/agent/"
        )

        self.connection = webrtc_python.WebRtc(self.config)

    def accept(self):
        connection_handle = self.connection.accept_connection(10)

        data_channel = connection_handle.create_data_channel("data")
        control_channel = connection_handle.create_data_channel("control")

        client = {
            "connection_handle": connection_handle,
            "data_channel": data_channel,
            "control_channel": control_channel,
        }
        self.clients.append(client)

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

            self.connection_lock.acquire()

            for client in self.clients:
                client["data_channel"].send(chunk)

            self.connection_lock.release()

    def receive(self):
        # TODO: Implement for multiple clients
        if not self.clients:
            return
        client = self.clients[0]

        buffer = bytearray(1000)
        bytes_read = 0

        def receive_data():
            global bytes_read
            bytes_read = client["data_channel"].receive(buffer)

        self.connection_lock.acquire()

        thread = threading.Thread(target=receive_data)
        thread.start()
        thread.join(0.01)

        self.connection_lock.release()

        if bytes_read > 0:
            return buffer[:bytes_read]
