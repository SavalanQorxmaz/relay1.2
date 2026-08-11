import json
from core.settings import (
    HANDSHAKE_REQUEST,
    HANDSHAKE_ACCEPT,
    HANDSHAKE_REJECT,
    HANDSHAKE_CANCEL,
)

class HandshakeService:
    @staticmethod
    def create_request(relay_id):
        return { "type": HANDSHAKE_REQUEST, "relay_id": relay_id }

    @staticmethod
    def create_accept():
        return { "type": HANDSHAKE_ACCEPT }

    @staticmethod
    def create_reject():
        return { "type": HANDSHAKE_REJECT }

    @staticmethod
    def create_cancel():
        return { "type": HANDSHAKE_CANCEL }

    @staticmethod
    def send(relay_socket, packet):
        # Paketin sonuna hökmən \n əlavə edirik
        data_str = json.dumps(packet) + "\n"
        data = data_str.encode("utf-8")
        print("[SEND]", data)
        relay_socket.sendall(data)

    @staticmethod
    def parse(data):
        try:
            # Gələn datanın ətrafındakı boşluqları və \n təmizləyirik
            clean_data = data.decode("utf-8").strip()
            if not clean_data:
                return None
            return json.loads(clean_data)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"[Handshake Parse Error] Yararsız data: {e}")
            return None
