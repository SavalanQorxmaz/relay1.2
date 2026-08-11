"""
Relay 1.2

Transfer Controller
"""

import hashlib
from pathlib import Path
from services.transfer.transfer_service import TransferService


class TransferController:

    def __init__(self, ui_manager):

        self.ui_manager = ui_manager

        self.transfer_panel = (
            ui_manager.transfer_panel
        )

        self.transfer_popup = (
            ui_manager.transfer_popup
        )

        self.selected_paths = []

        self.transfer_items = []

        self.bind_events()

    def bind_events(self):

        self.transfer_panel.set_selection_callback(
            self.load_selection
        )

        self.transfer_panel.set_send_callback(
            self.send_transfer
        )

    def load_selection(self):

        self.selected_paths = (
            self.transfer_panel.get_paths()
        )

        print(
            "[Transfer] Selected paths:"
        )

        for path in self.selected_paths:

            print(
                f"  {path}"
            )

        self.prepare_transfer_items()

    def prepare_transfer_items(self):

        self.transfer_items = []

        seen_files = set()

        for selected_path in self.selected_paths:

            path = Path(selected_path)

            if not path.exists():

                print(
                    f"[Transfer] Path does not exist: {path}"
                )

                continue

            # -------------------------
            # Single file
            # -------------------------

            if path.is_file():

                self.add_file(
                    path,
                    path.name,
                    seen_files
                )

            # -------------------------
            # Folder
            # -------------------------

            elif path.is_dir():

                for file_path in path.rglob("*"):

                    if not file_path.is_file():
                        continue

                    relative_path = (
                        path.name /
                        file_path.relative_to(path)
                    )

                    self.add_file(
                        file_path,
                        relative_path,
                        seen_files
                    )

        self.print_transfer_items()

    def add_file(
        self,
        file_path,
        relative_path,
        seen_files
    ):

        file_hash = self.calculate_hash(
            file_path
        )

        if not file_hash:

            return

        # -------------------------
        # Duplicate content
        # -------------------------

        if file_hash in seen_files:

            print(
                "[Transfer] Duplicate content skipped:"
            )

            print(
                f"  {file_path}"
            )

            return

        seen_files.add(
            file_hash
        )

        self.transfer_items.append({

            "source": file_path,

            "relative_path": str(
                relative_path
            ),

            "size": file_path.stat().st_size,

            "hash": file_hash

        })

    def calculate_hash(
        self,
        file_path
    ):

        sha256 = hashlib.sha256()

        try:

            with open(
                file_path,
                "rb"
            ) as file:

                while True:

                    chunk = file.read(
                        1024 * 1024
                    )

                    if not chunk:
                        break

                    sha256.update(
                        chunk
                    )

        except OSError as e:

            print(
                f"[Transfer] Hash error: "
                f"{file_path}"
            )

            print(e)

            return None

        return sha256.hexdigest()

    def print_transfer_items(self):

        print(
            "[Transfer] Prepared items:"
        )

        for item in self.transfer_items:

            print(
                f"  {item['relative_path']} "
                f"({item['size']} bytes)"
            )

            print(
                f"    SHA256: {item['hash']}"
            )

    def get_selected_paths(self):

        return list(
            self.selected_paths
        )

    def get_transfer_items(self):

        return list(
            self.transfer_items
        )

    def accept_transfer(self):

        print(
            "[Transfer] Accept clicked"
        )

        self.transfer_popup.hide()

        packet = TransferService.create_accept()

        self.ui_manager.connection_controller.send_transfer_packet(
            packet
        )


    def reject_transfer(self):

        print(
            "[Transfer] Reject clicked"
        )

        self.transfer_popup.hide()

        packet = TransferService.create_reject()

        self.ui_manager.connection_controller.send_transfer_packet(
            packet
        )

    def send_transfer(self):

        print(
            "[Transfer] Send requested"
        )

        if not self.transfer_items:

            print(
                "[Transfer] No transfer items"
            )

            return

        connection_controller = (
            self.ui_manager.connection_controller
        )

        if connection_controller.socket is None:

            print(
                "[Transfer] No active connection"
            )

            return

        packet = TransferService.create_request(
            self.transfer_items
        )

        if not connection_controller.send_transfer_packet(
            packet
        ):

            print(
                "[Transfer] Failed to send "
                "TRANSFER_REQUEST"
            )

            return

        print(
            "[Transfer] TRANSFER_REQUEST sent"
        )

        print(
            f"[Transfer] Items sent: "
            f"{len(packet['items'])}"
        )

    def test_incoming_transfer(self):

        self.transfer_popup.clear_items()

        self.transfer_popup.set_summary(
            folders=1,
            files=3,
            total_size="7.4 KB"
        )

        self.transfer_popup.add_item(
            "kompyuterler",
            "folder",
            "5 files"
        )

        self.transfer_popup.add_item(
            "README.md",
            "file",
            "3.2 KB"
        )

        self.transfer_popup.add_item(
            "sysspy.ico",
            "file",
            "4.2 KB"
        )

        self.transfer_popup.set_progress(
            0
        )

        self.transfer_popup.show()

    def receive_transfer_request(
        self,
        packet
    ):

        print(
            "[Transfer] Incoming transfer request"
        )

        items = packet.get(
            "items",
            []
        )

        if not items:

            print(
                "[Transfer] Empty transfer request"
            )

            return

        self.transfer_popup.clear_items()

        folders = set()
        files = []
        total_size = 0

        for item in items:

            relative_path = Path(
                item["relative_path"]
            )

            size = item["size"]

            total_size += size

            if len(relative_path.parts) > 1:

                folders.add(
                    relative_path.parts[0]
                )

            files.append(item)

        print(
            f"[Transfer] Incoming files: "
            f"{len(files)}"
        )

        print(
            f"[Transfer] Incoming folders: "
            f"{len(folders)}"
        )

        for folder in sorted(folders):

            folder_files = sum(
                1
                for item in files
                if Path(
                    item["relative_path"]
                ).parts[0] == folder
            )

            self.transfer_popup.add_item(
                folder,
                "folder",
                f"{folder_files} files"
            )

        for item in files:

            relative_path = Path(
                item["relative_path"]
            )

            # Qovluqdakı faylı ayrıca popup-da göstərmirik.
            if len(relative_path.parts) > 1:

                continue

            self.transfer_popup.add_item(
                relative_path.name,
                "file",
                self.format_size(
                    item["size"]
                )
            )

        self.transfer_popup.set_summary(
            folders=len(folders),
            files=len(files),
            total_size=self.format_size(
                total_size
            )
        )

        self.transfer_popup.set_progress(
            0
        )

        self.transfer_popup.show()

    def format_size(self, size):

        if size < 1024:
            return f"{size} B"

        if size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"

        if size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.1f} MB"

        return f"{size / (1024 * 1024 * 1024):.1f} GB"

    