import tkinter as tk

class BasePanel(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.create_layout()

        self.create_widgets()

        self.place_widgets()

        self.bind_events()

    def create_layout(self):
        pass

    def create_widgets(self):
        pass

    def place_widgets(self):
        pass

    def bind_events(self):
        pass

    def show(self):

        self.pack(
            fill="both",
            expand=True
        )

    def hide(self):

        self.pack_forget()