from services.network_service import NetworkService
from services.firewall_service import FirewallService
from services.firewall_installer import FirewallInstaller
from services.receive_folder_service import ReceiveFolderService
from pathlib import Path
from tkinter import filedialog
from tkinter import messagebox
from core.settings import FIREWALL_CHECK_DELAY

from services.receive_folder_service import ReceiveFolderService


class HeaderController:

    def __init__(self, header_panel):

        self.header_panel = header_panel

        self.initialize()

    def initialize(self):

        self.load_relay_id()

        self.load_firewall_status()

        self.bind_events()

        path = ReceiveFolderService.get_path()

        display_path = (
            "...\\" +
            "\\".join(path.parts[-2:])
        )

        self.header_panel.receive_folder_widget.set_path(
            display_path
        )

        self.header_panel.receive_folder_widget.set_open_callback(
            self.open_receive_folder
        )

        self.header_panel.receive_folder_widget.set_change_callback(
            self.change_receive_folder
        )

    def load_relay_id(self):

        relay_id = NetworkService.get_relay_id()

        self.header_panel.relay_id_widget.set_id(
            relay_id
        )

    def load_firewall_status(self):

        status = FirewallService.get_status()

        self.header_panel.firewall_widget.set_status(
            status
        )

    def bind_events(self):

        self.header_panel.relay_id_widget.set_copy_callback(
            self.copy_relay_id
        )

        self.header_panel.firewall_widget.set_configure_callback(
            self.configure_firewall
        )

    def copy_relay_id(self):

        relay_id = NetworkService.get_relay_id()

        self.header_panel.clipboard_clear()

        self.header_panel.clipboard_append(relay_id)

        self.header_panel.update()

    def configure_firewall(self):

        FirewallInstaller.install()

        self.header_panel.after(
            FIREWALL_CHECK_DELAY,
            self.check_firewall_result
        )

    def check_firewall_result(self):

        self.load_firewall_status()

        status = FirewallService.get_status()

        if status != "Configured":

            messagebox.showwarning(
                "Firewall Configuration",
                (
                    "Automatic firewall configuration could not be completed.\n\n"
                    "You can export the Firewall Tool from the footer and "
                    "run it as Administrator."
                )
            )

    def open_receive_folder(self):

        ReceiveFolderService.open_folder()

    def change_receive_folder(self):

        current_path = ReceiveFolderService.get_path()

        selected = filedialog.askdirectory(
            title="Select Receive Folder",
            initialdir=str(current_path)
        )

        if not selected:
            return

        ReceiveFolderService.set_path(
            Path(selected)
        )

        path = Path(selected)

        display_path = (
            "...\\" +
            "\\".join(path.parts[-2:])
        )

        self.header_panel.receive_folder_widget.set_path(
            display_path
        )

    
    def show_connection_widget(
        self,
        relay_id
    ):

        self.header_panel.connection_widget.set_relay_id(
            relay_id
        )

        self.header_panel.connection_widget.show()

    def hide_connection_widget(self):

        self.header_panel.connection_widget.hide()

    def bind_connection_callback(self, callback):

        self.header_panel.connection_widget.set_disconnect_callback(
            callback
        )