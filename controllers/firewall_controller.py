from services.firewall_service import FirewallService


class FirewallController:

    def __init__(self, header_panel):

        self.header_panel = header_panel

        self.initialize()

    def initialize(self):

        status = FirewallService.get_status()

        self.header_panel.firewall_widget.set_status(
            status
        )