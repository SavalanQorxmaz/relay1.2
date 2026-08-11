import tkinter as tk

from ui.widgets.base_widget import BaseWidget


class ReceiveFolderWidget(BaseWidget):

    def create_layout(self):

        self.grid_columnconfigure(
            0,
            weight=1
        )

    def create_widgets(self):

        self.title_label = tk.Label(
            self,
            text="Receive Folder",
            anchor="w",
            bg=self.cget("bg")
        )

        self.path_label = tk.Label(
            self,
            text="--------",
            anchor="w",
            bg=self.cget("bg"),
            font=("Segoe UI", 10)
        )

        self.open_button = tk.Button(
            self,
            text="Open",
            cursor="hand2"
        )

        self.change_button = tk.Button(
            self,
            text="Change",
            cursor="hand2"
        )

    def place_widgets(self):

        self.title_label.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w"
        )

        self.path_label.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(4, 0)
        )

        self.open_button.grid(
            row=2,
            column=0,
            pady=(8, 0),
            sticky="w"
        )

        self.change_button.grid(
            row=2,
            column=1,
            padx=(8, 0),
            pady=(8, 0),
            sticky="w"
        )

    def set_path(self, path: str):

        self.path_label.configure(
            text=path
        )

    def bind_events(self):

        self.open_button.configure(
            command=self.on_open_clicked
        )

        self.change_button.configure(
            command=self.on_change_clicked
        )

    def on_open_clicked(self):

        if hasattr(self, "open_callback"):
            self.open_callback()

    def on_change_clicked(self):

        if hasattr(self, "change_callback"):
            self.change_callback()

    def set_open_callback(self, callback):

        self.open_callback = callback

    def set_change_callback(self, callback):

        self.change_callback = callback