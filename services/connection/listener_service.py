

"""
Relay 1.2

Listener Service
"""

import socket
import threading


class ListenerService:

    def __init__(self, port):

        self.port = port

        self.listener_socket = None

        self.listener_thread = None

        self.running = False

        self.on_connected = None

    def start(self):

        print("[Listener] start() called")

        if self.running:
            print("[Listener] Already running")
            return

        self.listener_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        self.listener_socket.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        self.listener_socket.bind(
            ("", self.port)
        )

        self.listener_socket.listen(1)

        self.running = True

        self.listener_thread = threading.Thread(
            target=self.listen_loop,
            daemon=True
        )

        self.listener_thread.start()

        print(
            f"[Listener] Listening on {self.port}"
        )

    def listen_loop(self):

        while self.running:

            try:

                peer_socket, peer_address = (
                    self.listener_socket.accept()
                )

            except OSError:
                break

            print(
                f"[Listener] Incoming Connection: {peer_address}"
            )

            if self.on_connected:

                self.on_connected(
                    peer_socket,
                    peer_address
                )

            else:

                peer_socket.close()

    def stop(self):

        self.running = False

        if self.listener_socket:

            try:

                self.listener_socket.close()

            except OSError:
                pass

            self.listener_socket = None
            self.listener_thread = None