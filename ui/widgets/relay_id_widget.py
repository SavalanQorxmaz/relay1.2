import tkinter as tk

from ui.widgets.base_widget import BaseWidget


class RelayIdWidget(BaseWidget):

    def create_layout(self):

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_columnconfigure(
            1,
            weight=0
        )

    def create_widgets(self):

        self.title_label = tk.Label(
            self,
            text="Relay ID",
            anchor="w",
            bg=self.cget("bg")
        )

        self.id_label = tk.Label(
            self,
            text="-------- ----",
            anchor="w",
            bg=self.cget("bg"),
            font=("Consolas", 11, "bold")
        )

        self.copy_button = tk.Button(
            self,
            text="📋",
            relief="flat",
            bd=0,
            highlightthickness=0,
            padx=2,
            pady=0,
            cursor="hand2"
        )

    def place_widgets(self):

        self.title_label.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(0, 4)
        )

        self.id_label.grid(
            row=1,
            column=0,
            sticky="w"
        )

        self.copy_button.grid(
            row=1,
            column=1,
            sticky="e",
            padx=(6, 0)
        )

    def set_id(self, relay_id: str):

        self.id_label.configure(
            text=relay_id
        )

    def bind_events(self):

        self.copy_button.configure(
            command=self.on_copy_clicked
        )


    def on_copy_clicked(self):

        if hasattr(self, "copy_callback"):

            self.copy_callback()

    def set_copy_callback(self, callback):

        self.copy_callback = callback