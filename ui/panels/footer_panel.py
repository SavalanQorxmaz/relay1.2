import tkinter as tk


from ui.panels.base_panel import BasePanel
from controllers.footer_controller import FooterController


class FooterPanel(BasePanel):

    FOOTER_BG = "#F2F2F2"

    def create_layout(self):

        self.configure(
            bg=self.FOOTER_BG
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_columnconfigure(
            1,
            weight=0
        )

        self.grid_columnconfigure(
            2,
            weight=0
        )

        self.grid_columnconfigure(
            3,
            weight=0
        )

    def create_widgets(self):

        self.version_label = tk.Label(
            self,
            text="Relay 1.2",
            bg=self.FOOTER_BG,
            fg="#777777"
        )

        self.about_label = tk.Label(
            self,
            text="About",
            bg=self.FOOTER_BG,
            fg="#0066CC",
            cursor="hand2"
        )

        self.help_label = tk.Label(
            self,
            text="Help",
            bg=self.FOOTER_BG,
            fg="#0066CC",
            cursor="hand2"
        )

        self.firewall_button = tk.Button(
            self,
            text="Download Firewall Tool",
            cursor="hand2"
        )

    def place_widgets(self):

        self.version_label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=10,
            pady=8
        )

        self.about_label.grid(
            row=0,
            column=1,
            padx=(0, 12)
        )

        self.help_label.grid(
            row=0,
            column=2,
            padx=(0, 12)
        )

        self.firewall_button.grid(
            row=0,
            column=3,
            padx=10,
            pady=4
        )

    def bind_events(self):

        self.controller = FooterController(self)

        for widget in (
            self.about_label,
            self.help_label
        ):

            widget.bind(
                "<Enter>",
                self.on_link_enter
            )

            widget.bind(
                "<Leave>",
                self.on_link_leave
            )

        self.about_label.bind(
            "<Button-1>",
            lambda e: self.controller.show_about()
        )

        self.help_label.bind(
            "<Button-1>",
            lambda e: self.controller.show_help()
        )

    def on_link_enter(self, event):

        event.widget.configure(
            fg="#004C99"
        )

    def on_link_leave(self, event):

        event.widget.configure(
            fg="#0066CC"
        )