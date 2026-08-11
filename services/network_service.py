"""
Relay 1.2

Network Service

Provides local network information.
"""

import socket

from services.relay_id_service import RelayIdService


class NetworkService:

    @staticmethod
    def get_local_ip() -> str:
        """
        Return the active local IPv4 address.
        """

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        try:

            sock.connect(
                ("8.8.8.8", 80)
            )

            ip = sock.getsockname()[0]

        finally:

            sock.close()

        return ip

    @staticmethod
    def get_relay_id() -> str:
        """
        Return Relay ID generated from local IP.
        """

        ip = NetworkService.get_local_ip()

        return RelayIdService.ip_to_id(ip)