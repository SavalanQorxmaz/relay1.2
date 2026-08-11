
"""
Relay 1.2

Transfer Panel
"""

import tkinter as tk
from tkinter import filedialog

from ui.panels.base_panel import BasePanel


class TransferPanel(BasePanel):

    def create_layout(self):

        self.configure(
            bg="#F2F2F2"
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            1,
            weight=1
        )

    def create_widgets(self):

        # -------------------------
        # Title
        # -------------------------

        self.title_label = tk.Label(
            self,
            text="Files to send",
            bg=self.cget("bg"),
            font=("Segoe UI", 11, "bold")
        )

        # -------------------------
        # Buttons
        # -------------------------

        self.button_frame = tk.Frame(
            self,
            bg=self.cget("bg")
        )

        self.add_files_button = tk.Button(
            self.button_frame,
            text="Add Files"
        )

        self.add_folder_button = tk.Button(
            self.button_frame,
            text="Add Folder"
        )

        self.remove_button = tk.Button(
            self.button_frame,
            text="Remove Selected"
        )

        self.clear_button = tk.Button(
            self.button_frame,
            text="Clear"
        )

        self.send_button = tk.Button(
            self.button_frame,
            text="Send"
        )

        # -------------------------
        # Selection list
        # -------------------------

        self.list_frame = tk.Frame(
            self,
            bg=self.cget("bg")
        )

        self.path_listbox = tk.Listbox(
            self.list_frame,
            selectmode=tk.EXTENDED
        )

        # -------------------------
        # Callbacks
        # -------------------------

        self.on_selection_changed = None
        self.on_send = None

        self.scrollbar = tk.Scrollbar(
            self.list_frame,
            orient=tk.VERTICAL,
            command=self.path_listbox.yview
        )

        self.path_listbox.configure(
            yscrollcommand=self.scrollbar.set
        )

    def place_widgets(self):

        self.title_label.grid(
            row=0,
            column=0,
            padx=15,
            pady=(15, 8),
            sticky="w"
        )

        self.button_frame.grid(
            row=0,
            column=0,
            padx=15,
            pady=(10, 10),
            sticky="e"
        )

        self.add_files_button.grid(
            row=0,
            column=0,
            padx=4
        )

        self.add_folder_button.grid(
            row=0,
            column=1,
            padx=4
        )

        self.remove_button.grid(
            row=0,
            column=2,
            padx=4
        )

        self.clear_button.grid(
            row=0,
            column=3,
            padx=4
        )

        self.send_button.grid(
            row=0,
            column=4,
            padx=10
        )

        self.list_frame.grid(
            row=1,
            column=0,
            padx=15,
            pady=(0, 15),
            sticky="nsew"
        )

        self.list_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.list_frame.grid_rowconfigure(
            0,
            weight=1
        )

        self.path_listbox.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

    def bind_events(self):

        self.add_files_button.configure(
            command=self.add_files
        )

        self.add_folder_button.configure(
            command=self.add_folder
        )

        self.remove_button.configure(
            command=self.remove_selected
        )

        self.clear_button.configure(
            command=self.clear
        )

        self.send_button.configure(
            command=self.send_clicked
        )

    # -------------------------
    # File selection
    # -------------------------

    def add_files(self):

        paths = filedialog.askopenfilenames(
            title="Select files"
        )

        for path in paths:

            self.add_path(path)

    # -------------------------
    # Folder selection
    # -------------------------

    def add_folder(self):

        path = filedialog.askdirectory(
            title="Select folder"
        )

        if not path:
            return

        self.add_path(path)

    # -------------------------
    # Add path
    # -------------------------

    def add_path(self, path):

        existing = self.path_listbox.get(
            0,
            tk.END
        )

        if path in existing:
            return

        self.path_listbox.insert(
            tk.END,
            path
        )

        if self.on_selection_changed:

            self.on_selection_changed()

    # -------------------------
    # Remove selected
    # -------------------------

    def remove_selected(self):

        selected = self.path_listbox.curselection()

        for index in reversed(selected):

            self.path_listbox.delete(
                index
            )

        if self.on_selection_changed:

            self.on_selection_changed()

    # -------------------------
    # Clear
    # -------------------------

    def clear(self):

        self.path_listbox.delete(
            0,
            tk.END
        )

        if self.on_selection_changed:

            self.on_selection_changed()

    # -------------------------
    # Get selected paths
    # -------------------------

    def get_paths(self):

        return list(
            self.path_listbox.get(
                0,
                tk.END
            )
        )

    # -------------------------
    # Selection callback
    # -------------------------

    def set_selection_callback(self, callback):

        self.on_selection_changed = callback

    # -------------------------
    # Send callback
    # -------------------------

    def set_send_callback(self, callback):

        self.on_send = callback

    # -------------------------
    # Send clicked
    # -------------------------

    def send_clicked(self):

        if self.on_send:

            self.on_send()
