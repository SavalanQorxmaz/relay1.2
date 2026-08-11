import tkinter as tk

from ui.widgets.base_widget import BaseWidget


class FirewallWidget(BaseWidget):

    STATUS_COLORS = {
        "Configured": "#2ECC71",
        "Not Configured": "#F1C40F",
        "Error": "#E74C3C",
    }

    def create_layout(self):

        self.grid_columnconfigure(
            1,
            weight=1
        )

    def create_widgets(self):

        self.title_label = tk.Label(
            self,
            text="Firewall",
            bg=self.cget("bg"),
            anchor="w"
        )

        self.indicator = tk.Label(
            self,
            text="●",
            bg=self.cget("bg"),
            fg="#F1C40F",
            font=("Segoe UI", 12, "bold")
        )

        self.status_label = tk.Label(
            self,
            text="Not Configured",
            bg=self.cget("bg"),
            anchor="w"
        )

        self.configure_button = tk.Button(
            self,
            text="Configure",
            cursor="hand2"
        )

        self.refresh_button = tk.Button(
            self,
            text="Refresh",
            cursor="hand2"
        )

    def place_widgets(self):

        self.title_label.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="w"
        )

        self.indicator.grid(
            row=1,
            column=0,
            pady=(4, 0),
            sticky="w"
        )

        self.status_label.grid(
            row=1,
            column=1,
            padx=(6, 10),
            pady=(4, 0),
            sticky="w"
        )

        self.configure_button.grid(
            row=1,
            column=2,
            padx=(10, 5),
            sticky="w"
        )

        self.refresh_button.grid(
            row=1,
            column=3,
            sticky="w"
        )

    def set_status(self, status: str):

        self.status_label.configure(
            text=status
        )

        self.indicator.configure(
            fg=self.STATUS_COLORS.get(
                status,
                self.STATUS_COLORS["Error"]
            )
        )

        if status == "Configured":

            self.configure_button.grid_remove()
            self.refresh_button.grid_remove()

        else:

            self.configure_button.grid()
            self.refresh_button.grid()

    def bind_events(self):

        self.configure_button.configure(
            command=self.on_configure_clicked
        )

        self.refresh_button.configure(
            command=self.on_refresh_clicked
        )

    def on_configure_clicked(self):

        if hasattr(self, "configure_callback"):

            self.configure_callback()

    def set_configure_callback(self, callback):

        self.configure_callback = callback

    def on_refresh_clicked(self):

        if hasattr(self, "refresh_callback"):

            self.refresh_callback()

    def set_refresh_callback(self, callback):

        self.refresh_callback = callback