from ui.panels.base_panel import BasePanel
from ui.widgets.receive_folder_widget import ReceiveFolderWidget
from ui.widgets.relay_id_widget import RelayIdWidget
from ui.widgets.firewall_widget import FirewallWidget
from ui.widgets.connection_widget import ConnectionWidget
from controllers.header_controller import HeaderController


class HeaderPanel(BasePanel):

    DEBUG_COLOR = "#F2F2F2"

    def create_layout(self):

        self.configure(
            bg=self.DEBUG_COLOR
        )

        # Relay
        self.grid_columnconfigure(0, weight=0)

        # Spacer
        self.grid_columnconfigure(1, weight=1)

        # Firewall
        self.grid_columnconfigure(2, weight=0)

        # Big Spacer
        self.grid_columnconfigure(3, weight=1)

        # Connection
        self.grid_columnconfigure(4, weight=0)

        # Small Spacer
        self.grid_columnconfigure(5, weight=0)

        # Receive Folder
        self.grid_columnconfigure(6, weight=0)

    def create_widgets(self):

        self.relay_id_widget = RelayIdWidget(self)

        self.firewall_widget = FirewallWidget(self)

        self.connection_widget = ConnectionWidget(self)

        self.receive_folder_widget = ReceiveFolderWidget(self)

    def place_widgets(self):

        self.relay_id_widget.grid(
            row=0,
            column=0,
            padx=15,
            pady=10,
            sticky="w"
        )

        self.firewall_widget.grid(
            row=0,
            column=2,
            padx=15,
            pady=10
        )

        self.connection_widget.grid(
            row=0,
            column=4,
            padx=(0, 15),
            pady=10
        )

        self.connection_widget.hide()

        self.receive_folder_widget.grid(
            row=0,
            column=6,
            padx=15,
            pady=10,
            sticky="e"
        )

    def bind_events(self):

        self.controller = HeaderController(self)