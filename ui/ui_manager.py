import tkinter as tk
from app_state import AppState
from controllers.transfer_controller import TransferController
from ui.panels.transfer_popup import TransferPopup
from ui.panels.header_panel import HeaderPanel
from ui.panels.footer_panel import FooterPanel
from ui.panels.connection_popup import ConnectionPopup
from ui.panels.connection_panel import ConnectionPanel
from ui.panels.transfer_panel import TransferPanel
from services.connection.listener_service import ListenerService
from controllers.connection_controller import ConnectionController
from core.settings import RELAY_PORT


class UIManager:

    def __init__(self, root):

        print("[UIManager] __init__")

        self.root = root
        self.root.ui_manager = self

        self.current_state = AppState.READY

        self.connection_controller = ConnectionController(
            self
        )

        self.create_window()

        self.create_root_layout()

        self.create_panels()

        self.transfer_controller = TransferController(
            self
        )

        self.create_listener()

        self.bind_popup_events()

        self.header_panel.controller.bind_connection_callback(
            self.connection_controller.disconnect
        )

        self.render_panels()

    def create_window(self):

        self.root.title("Relay 1.2")

        self.root.geometry("900x700")

        self.root.minsize(800, 600)

    def create_root_layout(self):

        self.header_container = tk.Frame(
            self.root,
            bg=self.root.cget("bg"),
            height=60
        )

        self.body_container = tk.Frame(
            self.root,
            bg=self.root.cget("bg")
        )

        self.footer_container = tk.Frame(
            self.root,
            bg=self.root.cget("bg"),
            height=45
        )

        self.header_container.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        self.body_container.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.footer_container.grid(
            row=2,
            column=0,
            sticky="ew"
        )

        self.header_container.grid_propagate(False)
        self.footer_container.grid_propagate(False)

        self.root.grid_rowconfigure(
            1,
            weight=1
        )

        self.root.grid_columnconfigure(
            0,
            weight=1
        )

    def create_panels(self):

        self.header_panel = HeaderPanel(
            self.header_container
        )

        self.footer_panel = FooterPanel(
            self.footer_container
        )

        self.connection_panel = ConnectionPanel(
            self.body_container
        )

        self.transfer_panel = TransferPanel(
            self.body_container
        )


        self.connection_popup = ConnectionPopup(
            self.root
        )

        self.transfer_popup = TransferPopup(
            self.root
        )

    def render_panels(self):

        self.header_panel.show()

        self.footer_panel.show()
        self.connection_popup.hide()
        self.transfer_popup.hide()

        self.set_state(
            AppState.READY
        )

    def set_state(self, state):

        self.current_state = state

        if state == AppState.READY:

            self.connection_popup.hide()

            self.connection_panel.show()
            self.transfer_panel.hide()

            self.header_panel.controller.hide_connection_widget()


        elif state == AppState.OUTGOING_REQUEST:

            self.connection_panel.hide()
            self.transfer_panel.hide()

            self.connection_popup.show_waiting(
                self.connection_controller.target_relay_id
            )


        elif state == AppState.INCOMING_REQUEST:

            self.connection_panel.hide()
            self.transfer_panel.hide()

            self.connection_popup.show_incoming(
                self.connection_controller.peer_relay_id
            )
            
        elif state == AppState.CONNECTED:

            self.connection_popup.hide()
            self.transfer_popup.hide()
            self.connection_panel.hide()
            self.transfer_panel.show()

            self.header_panel.controller.show_connection_widget(
                self.connection_controller.peer_relay_id
            )

        elif state == AppState.ERROR:

            self.connection_popup.hide()

            self.connection_panel.show()
            self.transfer_panel.hide()

            self.header_panel.controller.hide_connection_widget()

    def create_listener(self):

        print("[UIManager] create_listener")

        self.listener_service = ListenerService(
            RELAY_PORT
        )

        self.listener_service.on_connected = (
            self.connection_controller.start_incoming
        )

        self.listener_service.start()

    def bind_popup_events(self):

        self.connection_popup.set_accept_callback(
            self.connection_controller.accept_connection
        )

        self.connection_popup.set_reject_callback(
            self.connection_controller.reject_connection
        )

        self.connection_popup.set_cancel_callback(
            self.connection_controller.cancel_connection
        )

        self.transfer_popup.set_accept_callback(
            self.transfer_controller.accept_transfer
        )

        self.transfer_popup.set_reject_callback(
            self.transfer_controller.reject_transfer
        )