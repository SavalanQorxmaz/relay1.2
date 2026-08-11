"""
Relay 1.2

Connection Service
"""

import socket

from core.settings import RELAY_PORT
from services.relay_id_service import RelayIdService


class ConnectionService:

    CONNECTION_TIMEOUT = 3

    @classmethod
    def connect_to_relay(
        cls,
        relay_id: str
    ):

        relay_id = relay_id.strip()

        if not RelayIdService.is_valid_relay_id(
            relay_id
        ):
            return False, "Invalid Relay ID."

        ip = RelayIdService.id_to_ip(
            relay_id
        )

        if not RelayIdService.is_valid_ip(
            ip
        ):
            return False, "Invalid IP."

        relay_socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        relay_socket.settimeout(
            cls.CONNECTION_TIMEOUT
        )

        try:

            relay_socket.connect(
                (
                    ip,
                    RELAY_PORT
                )
            )

            print(
                f"[Connection] Connected to {ip}:{RELAY_PORT}"
            )

            return True, relay_socket

        except OSError:

            relay_socket.close()

            print(
                f"[Connection] Failed to connect {ip}:{RELAY_PORT}"
            )

            return False, "Relay not found."