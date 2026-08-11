
"""
Relay 1.2

File Transfer Service
"""

from pathlib import Path

from services.transfer.transfer_service import TransferService


class FileTransferService:

    CHUNK_SIZE = 64 * 1024

    def __init__(self, sock):

        self.socket = sock

    # -------------------------
    # Send complete file
    # -------------------------

    def send_file(
        self,
        file_item,
        send_packet,
        on_progress=None
    ):

        source = Path(
            file_item["source"]
        )

        relative_path = (
            file_item["relative_path"]
        )

        file_size = (
            file_item["size"]
        )

        file_hash = (
            file_item["hash"]
        )

        print(
            "[Transfer] Sending file:"
        )

        print(
            f"  {relative_path}"
        )

        print(
            f"  Size: {file_size} bytes"
        )

        # -------------------------
        # file_start
        # -------------------------

        start_packet = (
            TransferService.create_file_start(
                relative_path,
                file_size,
                file_hash
            )
        )

        if not send_packet(
            start_packet
        ):

            raise OSError(
                "Could not send file_start"
            )

        # -------------------------
        # Binary data
        # -------------------------

        sent = 0

        try:

            with open(
                source,
                "rb"
            ) as file:

                while True:

                    chunk = file.read(
                        self.CHUNK_SIZE
                    )

                    if not chunk:

                        break

                    self.socket.sendall(
                        chunk
                    )

                    sent += len(
                        chunk
                    )

                    print(
                        "[Transfer] File progress:"
                        f" {sent}/{file_size}"
                    )

                    if on_progress:

                        on_progress(
                            sent,
                            file_size
                        )

        except OSError:

            print(
                "[Transfer] File read/send error:"
            )

            print(
                source
            )

            raise

        # -------------------------
        # Verify local size
        # -------------------------

        if sent != file_size:

            raise OSError(
                "File size changed during transfer"
            )

        # -------------------------
        # file_end
        # -------------------------

        end_packet = (
            TransferService.create_file_end(
                relative_path,
                file_hash
            )
        )

        if not send_packet(
            end_packet
        ):

            raise OSError(
                "Could not send file_end"
            )

        print(
            "[Transfer] File sent successfully:"
        )

        print(
            f"  {relative_path}"
        )

    # -------------------------
    # Send multiple files
    # -------------------------

    def send_files(
        self,
        items,
        send_packet,
        on_file_start=None,
        on_progress=None,
        on_file_complete=None,
        on_file_error=None
    ):

        total_files = len(
            items
        )

        for index, item in enumerate(
            items,
            start=1
        ):

            relative_path = (
                item["relative_path"]
            )

            if on_file_start:

                on_file_start(
                    index,
                    total_files,
                    item
                )

            try:

                def file_progress(
                    sent,
                    size
                ):

                    if on_progress:

                        on_progress(
                            index,
                            total_files,
                            item,
                            sent,
                            size
                        )

                self.send_file(
                    item,
                    send_packet,
                    on_progress=file_progress
                )

                if on_file_complete:

                    on_file_complete(
                        index,
                        total_files,
                        item
                    )

            except Exception as e:

                print(
                    "[Transfer] File failed:"
                )

                print(
                    f"  {relative_path}"
                )

                print(
                    f"  Error: {e}"
                )

                if on_file_error:

                    on_file_error(
                        index,
                        total_files,
                        item,
                        e
                    )

                # Bir fayl uğursuz olsa belə
                # növbəti fayla keçirik.

                continue

    # -------------------------
    # Send JSON packet
    # -------------------------

    def send_json_packet(
        self,
        packet
    ):

        return self._send_packet(
            packet
        )

    def _send_packet(
        self,
        packet
    ):

        data = (
            TransferService.encode(
                packet
            )
        )

        try:

            self.socket.sendall(
                data
            )

            return True

        except OSError as e:

            print(
                "[Transfer] Packet send error:"
            )

            print(e)

            return False

