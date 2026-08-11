import tkinter as tk

from ui.panels.base_panel import BasePanel
from controllers.connect_controller import ConnectionController


class ConnectionPanel(BasePanel):

    DEBUG_COLOR = "#F2F2F2"

    def create_layout(self):

        self.configure(
            bg=self.DEBUG_COLOR
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

    def create_widgets(self):

        self.title_label = tk.Label(
            self,
            text="Connection",
            font=("Segoe UI", 14, "bold"),
            bg=self.DEBUG_COLOR
        )

        self.relay_id_label = tk.Label(
            self,
            text="Relay ID",
            bg=self.DEBUG_COLOR
        )

        self.relay_id_entry = tk.Entry(
            self,
            width=30
        )

        self.search_button = tk.Button(
            self,
            text="Search",
            width=12
        )

        self.status_title = tk.Label(
            self,
            text="Status",
            bg=self.DEBUG_COLOR
        )

        self.status_label = tk.Label(
            self,
            text="Waiting...",
            fg="#777777",
            bg=self.DEBUG_COLOR
        )

    def place_widgets(self):

        self.title_label.grid(
            row=0,
            column=0,
            pady=(30, 20)
        )

        self.relay_id_label.grid(
            row=1,
            column=0,
            pady=(10, 5)
        )

        self.relay_id_entry.grid(
            row=2,
            column=0,
            padx=20,
            sticky="ew"
        )

        self.search_button.grid(
            row=3,
            column=0,
            pady=20
        )

        self.status_title.grid(
            row=4,
            column=0,
            pady=(20, 5)
        )

        self.status_label.grid(
            row=5,
            column=0
        )

    def bind_events(self):

        self.controller = ConnectionController(
            self,
            self.winfo_toplevel().ui_manager
        )

        self.relay_id_entry.bind(
            "<Return>",
            lambda e: self.controller.search()
        )