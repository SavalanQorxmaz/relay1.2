"""
Relay 1.2

Transfer Service
"""

import json


class TransferService:

    # -------------------------
    # Packet types
    # -------------------------

    TRANSFER_REQUEST = "transfer_request"
    TRANSFER_ACCEPT = "transfer_accept"
    TRANSFER_REJECT = "transfer_reject"

    FILE_START = "file_start"
    FILE_END = "file_end"
    FILE_ERROR = "file_error"

    TRANSFER_COMPLETE = "transfer_complete"

    # -------------------------
    # Transfer request
    # -------------------------

    @staticmethod
    def create_request(items):

        return {
            "type": TransferService.TRANSFER_REQUEST,
            "items": [
                {
                    "relative_path": item["relative_path"],
                    "size": item["size"],
                    "hash": item["hash"]
                }
                for item in items
            ]
        }

    # -------------------------
    # Accept
    # -------------------------

    @staticmethod
    def create_accept():

        return {
            "type": TransferService.TRANSFER_ACCEPT
        }

    # -------------------------
    # Reject
    # -------------------------

    @staticmethod
    def create_reject():

        return {
            "type": TransferService.TRANSFER_REJECT
        }

    # -------------------------
    # File start
    # -------------------------

    @staticmethod
    def create_file_start(
        relative_path,
        size,
        file_hash
    ):

        return {
            "type": TransferService.FILE_START,
            "relative_path": relative_path,
            "size": size,
            "hash": file_hash
        }

    # -------------------------
    # File end
    # -------------------------

    @staticmethod
    def create_file_end(
        relative_path,
        file_hash
    ):

        return {
            "type": TransferService.FILE_END,
            "relative_path": relative_path,
            "hash": file_hash
        }

    # -------------------------
    # File error
    # -------------------------

    @staticmethod
    def create_file_error(
        relative_path,
        error
    ):

        return {
            "type": TransferService.FILE_ERROR,
            "relative_path": relative_path,
            "error": str(error)
        }

    # -------------------------
    # Transfer complete
    # -------------------------

    @staticmethod
    def create_complete():

        return {
            "type": TransferService.TRANSFER_COMPLETE
        }

    # -------------------------
    # JSON encode
    # -------------------------

    @staticmethod
    def encode(packet):

        return (
            json.dumps(
                packet,
                ensure_ascii=False
            )
            + "\n"
        ).encode("utf-8")

    # -------------------------
    # JSON decode
    # -------------------------

    @staticmethod
    def decode(data):

        try:

            return json.loads(
                data.decode("utf-8")
            )

        except (
            json.JSONDecodeError,
            UnicodeDecodeError
        ):

            return None