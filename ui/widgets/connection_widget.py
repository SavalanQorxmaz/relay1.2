import tkinter as tk

from ui.widgets.base_widget import BaseWidget


class ConnectionWidget(BaseWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.on_disconnect = None

    WIDTH = 260
    HEIGHT = 90

    def create_layout(self):

        self.grid_columnconfigure(0, weight=1)

    def create_widgets(self):

        self.title_label = tk.Label(
            self,
            text="Connected",
            bg=self.cget("bg"),
            font=("Segoe UI", 9, "bold")
        )

        self.relay_id_label = tk.Label(
            self,
            text="",
            bg=self.cget("bg")
        )

        self.disconnect_button = tk.Button(
            self,
            text="Disconnect",
            command=self.disconnect_clicked
        )

    def place_widgets(self):

        self.title_label.grid(
            row=0,
            column=0,
            pady=(6,2)
        )

        self.relay_id_label.grid(
            row=1,
            column=0,
            pady=2
        )

        self.disconnect_button.grid(
            row=2,
            column=0,
            pady=(6,6)
        )

        self.hide()

    def bind_events(self):
        pass

    def show(self):

        self.grid()

    def hide(self):

        self.grid_remove()

    def set_relay_id(self, relay_id):

        self.relay_id_label.configure(
            text=relay_id
        )

    def set_disconnect_callback(self, callback):

        self.on_disconnect = callback


    def disconnect_clicked(self):

        if self.on_disconnect:

            self.on_disconnect()

    