import tkinter as tk


class BaseWidget(tk.Frame):

    WIDTH = 240
    HEIGHT = 50

    def __init__(self, parent):

        super().__init__(
            parent,
            bg=parent.cget("bg"),
            width=self.WIDTH,
            height=self.HEIGHT,
            highlightbackground="#D6D6D6",
            highlightthickness=1
        )

        self.grid_propagate(False)

        self.create_layout()
        self.create_widgets()
        self.place_widgets()
        self.bind_events()