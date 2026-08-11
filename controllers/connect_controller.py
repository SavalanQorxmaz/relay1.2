"""
Relay 1.2

Connection Controller
"""

from services.connection.connection_service import ConnectionService
from ui import ui_manager
from app_state import AppState


class ConnectionController:

    def __init__(self, panel, ui_manager):

        self.panel = panel
        self.ui_manager = ui_manager
        self.connection_socket = None

        self.initialize()

    def initialize(self):

        self.panel.search_button.configure(
            command=self.search
        )

    def search(self):

        relay_id = self.panel.relay_id_entry.get()

        self.panel.status_label.configure(
            text="Searching..."
        )

        success, result = (
            ConnectionService.connect_to_relay(
                relay_id
            )
        )

        if success:

            self.connection_socket = result

            self.ui_manager.connection_controller.start_outgoing(
                result,
                relay_id
            )

        else:

            self.panel.status_label.configure(
                text=result
            )