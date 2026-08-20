"""
Relay 1.2

Connection Controller
"""
import threading
import hashlib
from pathlib import Path
import threading
import time
from services.transfer.file_transfer_service import FileTransferService

from app_state import AppState
from services.connection.handshake_service import HandshakeService
from services.network_service import NetworkService
from services.transfer.transfer_service import TransferService

from core.settings import (
    HANDSHAKE_REQUEST, 
    HANDSHAKE_ACCEPT,
    HANDSHAKE_REJECT,
    HANDSHAKE_CANCEL
)


class ConnectionController:

    def __init__(self, ui_manager):

        self.ui_manager = ui_manager

        self.socket = None

        self.peer_relay_id = None
        self.target_relay_id = None
        # -------------------------
        # Transfer receive state
        # -------------------------

        self.receive_buffer = bytearray()
        self.send_lock = threading.Lock()
        self.file_transfer_service = None
        self.current_file_relative_path = None
        self.current_file = None
        self.current_file_handle = None
        self.current_file_size = 0
        self.current_file_received = 0
        self.total_transfer_size = 0
        self.transferred_size = 0
        self.current_file_hash = None
        self.current_file_hasher = None
        self.waiting_for_file_end = False
        self.receive_root = (
            Path.cwd() / "received_files"
        )

    def start_outgoing( self, relay_socket, relay_id ):
        self.socket = relay_socket
        # Soketin gözləmə müddətini 60 saniyə edirik
        self.socket.settimeout(None) 
        
        self.target_relay_id = relay_id
        print("[Connection] Outgoing")
        self.ui_manager.set_state( AppState.OUTGOING_REQUEST )
        
        threading.Thread( target=self.receive_handshake, daemon=True ).start()
        threading.Thread( target=self.send_handshake, daemon=True ).start()

    def start_incoming( self, relay_socket, peer_address ):
        print("[Connection] start_incoming called")
        self.socket = relay_socket
        # Gələn qoşulma üçün də gözləmə müddətini 60 saniyə edirik
        self.socket.settimeout(None)
        
        print( f"[Connection] Incoming: {peer_address}" )
        thread = threading.Thread( target=self.receive_handshake, daemon=True )
        print("[Connection] Thread created")
        thread.start()
        print("[Connection] Thread started")


    def disconnect(self):

        if self.socket:

            try:

                packet = HandshakeService.create_cancel()

                HandshakeService.send(
                    self.socket,
                    packet
                )

                print("[Handshake] Cancel Sent")

            except OSError:

                print("[Connection] Peer already disconnected")

            try:

                self.socket.close()

            except OSError:
                pass

            self.socket = None

        self.peer_relay_id = None
        self.target_relay_id = None

        self.ui_manager.set_state(
            AppState.READY
        )

    def receive_handshake(self):

        buffer = ""

        while True:

            print("[Handshake] Waiting recv...")

            try:

                data = self.socket.recv(4096)

            except OSError as e:

                print(
                    f"[Handshake] OSError on recv. Sistem xətası: {e}"
                )

                print("[Handshake] Socket closed")

                break

            print("[Handshake] recv returned")

            if not data:

                print(
                    "[Handshake] Qarşı tərəf əlaqəni kəsdi (Empty data)"
                )

                self.ui_manager.set_state(
                    AppState.READY
                )

                break

            buffer += data.decode("utf-8")

            while "\n" in buffer:

                line, buffer = buffer.split("\n", 1)

                line = line.strip()

                if not line:
                    continue

                print(
                    f"[Handshake] Data parsing: {line}"
                )

                packet = HandshakeService.parse(
                    line.encode("utf-8")
                )

                if not packet:
                    continue

                packet_type = packet.get("type")

                print(
                    "packet_type =",
                    packet_type
                )

                # -----------------------------
                # REQUEST
                # -----------------------------

                if packet_type == HANDSHAKE_REQUEST:

                    print(
                        "[Handshake] Incoming request detected"
                    )

                    self.peer_relay_id = packet["relay_id"]

                    self.ui_manager.set_state(
                        AppState.INCOMING_REQUEST
                    )
                    return

                    # return YOXDUR
                    # Thread bağlantını dinləməyə davam edir.


                # -----------------------------
                # ACCEPT
                # -----------------------------

                elif packet_type == HANDSHAKE_ACCEPT:

                    print("[Handshake] Accepted")

                    if self.peer_relay_id is None:

                        self.peer_relay_id = (
                            self.target_relay_id
                        )

                    self.ui_manager.set_state(
                        AppState.CONNECTED
                    )

                    self.start_transfer_receiver()

                    return


                # -----------------------------
                # REJECT
                # -----------------------------

                elif packet_type == HANDSHAKE_REJECT:

                    print(
                        "[Handshake] Rejected"
                    )

                    try:

                        self.socket.close()

                    except OSError:
                        pass

                    self.socket = None

                    self.peer_relay_id = None
                    self.target_relay_id = None

                    self.ui_manager.set_state(
                        AppState.READY
                    )

                    return


                # -----------------------------
                # CANCEL
                # -----------------------------

                elif packet_type == HANDSHAKE_CANCEL:

                    print(
                        "[Handshake] Cancelled"
                    )

                    try:

                        self.socket.close()

                    except OSError:
                        pass

                    self.socket = None

                    self.peer_relay_id = None
                    self.target_relay_id = None

                    self.ui_manager.set_state(
                        AppState.READY
                    )

                    return



    def send_handshake(self):


        packet = HandshakeService.create_request(
            NetworkService.get_relay_id()
        )

        HandshakeService.send(
            self.socket,
            packet
        )

        print("[Handshake] Request Sent")


    def accept_connection(self):

        packet = HandshakeService.create_accept()

        HandshakeService.send(
            self.socket,
            packet
        )

        print("[Handshake] Accept Sent")

        self.ui_manager.set_state(
            AppState.CONNECTED
        )

        self.start_transfer_receiver()

    def reject_connection(self):

        packet = HandshakeService.create_reject()

        HandshakeService.send(
            self.socket,
            packet
        )

        print("[Handshake] Reject Sent")

        self.socket.close()

        self.ui_manager.set_state(
            AppState.READY
        )

    def cancel_connection(self):

        packet = HandshakeService.create_cancel()

        HandshakeService.send(
            self.socket,
            packet
        )

        print("[Handshake] Cancel Sent")

        self.socket.close()

        self.ui_manager.set_state(
            AppState.READY
        )

    def start_transfer_receiver(self):

        print("[Transfer] Receiver loop started")

        threading.Thread(
            target=self.receive_transfer_loop,
            daemon=True
        ).start()

    def receive_transfer_loop(self):

        print("[Transfer] Binary receiver started")

        self.receive_buffer = bytearray()

        while True:

            if self.socket is None:

                break

            try:

                data = self.socket.recv(64 * 1024)

            except OSError as e:

                print(
                    f"[Transfer] Receive error: {e}"
                )

                self.close_current_file()

                break

            if not data:

                print(
                    "[Transfer] Peer disconnected"
                )

                self.close_current_file()

                break

            self.receive_buffer.extend(data)

            while True:

                # -------------------------
                # Currently receiving file
                # -------------------------

                if self.current_file_handle:

                    if self.waiting_for_file_end:

                        newline_index = (
                            self.receive_buffer.find(
                                b"\n"
                            )
                        )

                        if newline_index == -1:

                            break

                        line = bytes(
                            self.receive_buffer[
                                :newline_index
                            ]
                        )

                        del self.receive_buffer[
                            :newline_index + 1
                        ]

                        line = line.strip()

                        if not line:
                            continue

                        packet = TransferService.decode(
                            line
                        )

                        if not packet:
                            print(
                                "[Transfer] Invalid packet"
                            )
                            continue

                        self.handle_transfer_packet(
                            packet
                        )

                        continue

                    remaining = (
                        self.current_file_size
                        - self.current_file_received
                    )

                    if remaining <= 0:
                        self.waiting_for_file_end = True

                        continue

                    chunk_size = min(
                        remaining,
                        len(self.receive_buffer)
                    )

                    if chunk_size <= 0:
                        break

                    chunk = bytes(
                        self.receive_buffer[
                            :chunk_size
                        ]
                    )

                    del self.receive_buffer[
                        :chunk_size
                    ]

                    try:

                        self.current_file_handle.write(
                            chunk
                        )

                        self.current_file_hasher.update(
                            chunk
                        )

                        self.current_file_received += (
                            chunk_size
                        )

                        self.update_transfer_progress()

                    except OSError as e:

                        print(
                            "[Transfer] "
                            f"File write error: "
                            f"{self.current_file}"
                        )

                        print(e)

                        self.handle_file_error(
                            str(e)
                        )

                    continue

                # -------------------------
                # Waiting for JSON packet
                # -------------------------

                newline_index = (
                    self.receive_buffer.find(
                        b"\n"
                    )
                )

                if newline_index == -1:

                    break

                line = bytes(
                    self.receive_buffer[
                        :newline_index
                    ]
                )

                del self.receive_buffer[
                    :newline_index + 1
                ]

                line = line.strip()

                if not line:

                    continue

                packet = TransferService.decode(
                    line
                )

                if not packet:

                    print(
                        "[Transfer] Invalid packet"
                    )

                    continue

                self.handle_transfer_packet(
                    packet
                )

    def handle_transfer_packet(
        self,
        packet
    ):

        packet_type = packet.get(
            "type"
        )

        print(
            f"[Transfer] Packet: {packet_type}"
        )

        # -------------------------
        # Transfer request
        # -------------------------

        if packet_type == (
            TransferService.TRANSFER_REQUEST
        ):

            self.ui_manager.transfer_controller.receive_transfer_request(
                packet
            )

        elif packet_type == (
            TransferService.TRANSFER_ACCEPT
        ):

            print(
                "[Transfer] Transfer accepted"
            )

            self.ui_manager.transfer_controller.transfer_popup.show()

            self.start_file_transfer()

        elif packet_type == (
            TransferService.TRANSFER_REJECT
        ):

            print(
                "[Transfer] Transfer rejected"
            )

        # -------------------------
        # File start
        # -------------------------

        elif packet_type == (
            TransferService.FILE_START
        ):

            self.start_incoming_file(
                packet
            )

        # -------------------------
        # File end
        # -------------------------

        elif packet_type == (
            TransferService.FILE_END
        ):

            self.handle_file_end(
                packet
            )

        # -------------------------
        # File error
        # -------------------------

        elif packet_type == (
            TransferService.FILE_ERROR
        ):

            print(
                "[Transfer] Sender reported "
                f"file error: "
                f"{packet.get('relative_path')}"
            )

            print(
                packet.get("error")
            )

        # -------------------------
        # Transfer complete
        # -------------------------

        elif packet_type == (
            TransferService.TRANSFER_COMPLETE
        ):

            print(
                "[Transfer] Transfer complete"
            )

            self.close_current_file()

    def send_transfer_packet(self, packet):

        if self.socket is None:

            print(
                "[Transfer] Socket unavailable"
            )

            return False

        try:

            data = TransferService.encode(
                packet
            )

            with self.send_lock:

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

    def start_file_transfer(self):

        if self.socket is None:

            print(
                "[Transfer] Cannot start:"
                " socket unavailable"
            )

            return

        items = (
            self.ui_manager
            .transfer_controller
            .get_transfer_items()
        )

        

        if not items:

            print(
                "[Transfer] No files to send"
            )

            return

        print(
            "[Transfer] Starting file transfer"
        )

        print(
            f"[Transfer] Total files: {len(items)}"
        )

        self.total_transfer_size = sum(
            item["size"]
            for item in items
        )

        self.transferred_size = 0

        self.file_transfer_service = (
            FileTransferService(
                self.socket
            )
        )

        threading.Thread(
            target=self._run_file_transfer,
            args=(items,),
            daemon=True
        ).start()

    def _run_file_transfer(
        self,
        items
    ):

        service = (
            self.file_transfer_service
        )

        try:

            service.send_files(
                items,
                self.send_transfer_packet,
                on_file_start=self.on_file_start,
                on_progress=self.on_file_progress,
                on_file_complete=self.on_file_complete,
                on_file_error=self.on_file_error
            )

            self.send_transfer_packet(
                TransferService.create_complete()
            )

            print(
                "[Transfer] All files processed"
            )

        except Exception as e:

            print(
                "[Transfer] Transfer error:"
            )

            print(e)

    def start_incoming_file(
        self,
        packet
    ):

        relative_path = packet.get(
            "relative_path"
        )

        size = packet.get(
            "size",
            0
        )

        file_hash = packet.get(
            "hash"
        )

        self.current_file_relative_path = relative_path

        if not relative_path:

            print(
                "[Transfer] Missing file path"
            )

            return

        try:

            size = int(size)

        except (
            TypeError,
            ValueError
        ):

            print(
                "[Transfer] Invalid file size"
            )

            return

        safe_path = self.get_safe_receive_path(
            relative_path
        )

        if safe_path is None:

            print(
                "[Transfer] Unsafe file path:"
            )

            print(relative_path)

            return

        try:

            safe_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            self.current_file_handle = open(
                safe_path,
                "wb"
            )

        except OSError as e:

            print(
                "[Transfer] Cannot create file:"
            )

            print(safe_path)
            print(e)

            self.current_file = None
            self.current_file_handle = None

            return

        self.current_file = safe_path

        self.current_file_size = size

        self.current_file_received = 0

        self.current_file_hash = file_hash
        self.waiting_for_file_end = False

        self.current_file_hasher = (
            hashlib.sha256()
        )

        print(
            "[Transfer] Receiving:"
        )

        print(
            f"  {relative_path}"
        )

        print(
            f"  Size: {size} bytes"
        )

    def get_safe_receive_path(
        self,
        relative_path
    ):

        try:

            relative = Path(
                relative_path
            )

            if relative.is_absolute():

                return None

            destination = (
                self.receive_root /
                relative
            ).resolve()

            root = (
                self.receive_root
                .resolve()
            )

            try:

                destination.relative_to(
                    root
                )

            except ValueError:

                return None

            return destination

        except (
            OSError,
            ValueError
        ):

            return None

    def finish_current_file(self):

        if not self.current_file_handle:

            return

        try:

            self.current_file_handle.flush()

            self.current_file_handle.close()

        except OSError as e:

            print(
                "[Transfer] File close error:"
            )

            print(e)

        self.current_file_handle = None

        calculated_hash = (
            self.current_file_hasher.hexdigest()
            if self.current_file_hasher
            else None
        )

        expected_hash = (
            self.current_file_hash
        )

        if calculated_hash == expected_hash:

            print(
                "[Transfer] File received successfully:"
            )

            print(
                f"  {self.current_file}"
            )

            print(
                "  SHA256: OK"
            )

        else:

            print(
                "[Transfer] SHA256 mismatch:"
            )

            print(
                f"  {self.current_file}"
            )

            print(
                f"  Expected: {expected_hash}"
            )

            print(
                f"  Received: {calculated_hash}"
            )

        self.current_file = None
        self.current_file_size = 0
        self.current_file_received = 0
        self.current_file_hash = None
        self.current_file_hasher = None
        self.current_file_relative_path = None

    def handle_file_end(
        self,
        packet
    ):

        relative_path = packet.get(
            "relative_path"
        )

        file_hash = packet.get(
            "hash"
        )

        print(
            "[Transfer] file_end:"
        )

        print(
            f"  {relative_path}"
        )

        if not self.current_file_handle:

            print(
                "[Transfer] No active file"
            )

            return

        if (
            self.current_file_received
            != self.current_file_size
        ):

            print(
                "[Transfer] Incomplete file:"
            )

            print(
                f"  Received: "
                f"{self.current_file_received}"
            )

            print(
                f"  Expected: "
                f"{self.current_file_size}"
            )

            self.handle_file_error(
                "Incomplete file"
            )

            return

        if (
            relative_path
            != self.get_current_relative_path()
        ):

            print(
                "[Transfer] FILE_END path mismatch:"
            )

            print(
                f"  Expected: "
                f"{self.get_current_relative_path()}"
            )

            print(
                f"  Received: "
                f"{relative_path}"
            )

            self.handle_file_error(
                "FILE_END path mismatch"
            )

            return

        if (
            file_hash
            != self.current_file_hash
        ):

            print(
                "[Transfer] FILE_END hash mismatch:"
            )

            print(
                f"  Expected: "
                f"{self.current_file_hash}"
            )

            print(
                f"  Received: "
                f"{file_hash}"
            )

            self.handle_file_error(
                "FILE_END hash mismatch"
            )

            return

        self.finish_current_file()

    def handle_file_error(
        self,
        error
    ):

        print(
            "[Transfer] File failed:"
        )

        print(
            f"  {self.current_file}"
        )

        print(
            f"  Error: {error}"
        )

        self.close_current_file()

    def close_current_file(self):

        if self.current_file_handle:

            try:

                self.current_file_handle.close()

            except OSError:
                pass

        self.current_file_handle = None

        self.current_file = None

        self.current_file_size = 0

        self.current_file_received = 0

        self.current_file_hash = None

        self.current_file_hasher = None
        self.current_file_relative_path = None

    def update_transfer_progress(self):

        if self.current_file_size <= 0:

            return

        progress = (
            self.current_file_received
            / self.current_file_size
        ) * 100

        print(
            "[Transfer] File progress:"
            f" {progress:.1f}%"
        )

        try:

            self.ui_manager.transfer_popup.set_progress(
                progress
            )

        except Exception as e:

            print(
                "[Transfer] Progress UI error:"
            )

            print(e)

    def on_file_start(
        self,
        index,
        total,
        item
    ):

        relative_path = str(
            item["relative_path"]
        )

        print(
            "[Transfer] File started:"
        )

        print(
            f"  [{index}/{total}] "
            f"{relative_path}"
        )

        self.ui_manager.root.after(
            0,
            lambda: self.ui_manager.transfer_popup.set_item_status_by_key(
                relative_path,
                "transferring"
            )
        )

    def on_file_progress(
        self,
        index,
        total,
        item,
        sent,
        size
    ):

        if size <= 0:

            return

        percent = (
            sent / size
        ) * 100

        print(
            "[Transfer] "
            f"[{index}/{total}] "
            f"{item['relative_path']} "
            f"{percent:.1f}%"
        )

    def on_file_complete(
        self,
        index,
        total,
        item
    ):

        relative_path = str(
            item["relative_path"]
        )

        print(
            "[Transfer] File completed:"
        )

        print(
            f"  [{index}/{total}] "
            f"{relative_path}"
        )

        self.ui_manager.root.after(
            0,
            lambda: self.ui_manager.transfer_popup.set_item_status_by_key(
                relative_path,
                "transferred"
            )
        )

    def on_file_error(
        self,
        index,
        total,
        item,
        error
    ):

        print(
            "[Transfer] File skipped:"
        )

        print(
            f"  [{index}/{total}] "
            f"{item['relative_path']}"
        )

        print(
            f"  Error: {error}"
        )

    def get_current_relative_path(self):

        return self.current_file_relative_path