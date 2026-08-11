import tkinter as tk

from ui.ui_manager import UIManager


class MainWindow:

    def __init__(self):

        self.root = tk.Tk()

        self.ui_manager = UIManager(self.root)

    def run(self):

        self.root.mainloop()