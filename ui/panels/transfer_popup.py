"""
Relay 1.2

Transfer Popup
"""

import tkinter as tk


class TransferPopup(tk.Toplevel):

    WIDTH = 520
    HEIGHT = 500

    def __init__(self, parent):

        super().__init__(parent)

        self.parent = parent

        self.on_accept = None
        self.on_reject = None
        self.item_status_labels = {}
        self.folder_items = {}
        self.withdraw()

        self.title("Incoming Transfer")

        self.resizable(False, False)

        self.transient(parent)

        self.protocol(
            "WM_DELETE_WINDOW",
            self.reject_clicked
        )

        self.create_layout()
        self.create_widgets()
        self.place_widgets()

    def create_widgets(self):

        self.title_label = tk.Label(
            self.content,
            text="Incoming Transfer",
            font=("Segoe UI", 12, "bold")
        )

        self.summary_label = tk.Label(
            self.content,
            text=""
        )

        self.list_frame = tk.Frame(
            self.content
        )

        self.progress_label = tk.Label(
            self.content,
            text="Progress: 0%"
        )

        self.progress = tk.DoubleVar(
            value=0
        )

        self.progress_bar = tk.Scale(
            self.content,
            variable=self.progress,
            from_=0,
            to=100,
            orient="horizontal",
            showvalue=False,
            state="disabled"
        )

        self.button_frame = tk.Frame(
            self.content
        )

        self.accept_button = tk.Button(
            self.button_frame,
            text="Accept",
            command=self.accept_clicked
        )

        self.reject_button = tk.Button(
            self.button_frame,
            text="Reject",
            command=self.reject_clicked
        )

    def create_layout(self):

        self.content = tk.Frame(
            self
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

    def place_widgets(self):

        self.title_label.pack(
            pady=(15, 5)
        )

        self.summary_label.pack(
            pady=(0, 10)
        )

        self.list_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=5
        )

        self.progress_label.pack(
            pady=(10, 2)
        )

        self.progress_bar.pack(
            fill="x",
            padx=25
        )

        self.button_frame.pack(
            pady=15
        )

        self.accept_button.pack(
            side="left",
            padx=10
        )

        self.reject_button.pack(
            side="left",
            padx=10
        )

    def set_accept_callback(self, callback):

        self.on_accept = callback

    def set_reject_callback(self, callback):

        self.on_reject = callback

    def accept_clicked(self):

        if self.on_accept:

            self.on_accept()

    def reject_clicked(self):

        if self.on_reject:

            self.on_reject()

    def show(self):

        self.center()

        self.deiconify()

        self.lift()

        self.grab_set()

        self.focus_force()

    def hide(self):

        try:

            self.grab_release()

        except tk.TclError:

            pass

        self.withdraw()

    def center(self):

        self.update_idletasks()

        x = (
            self.parent.winfo_rootx() +
            (
                self.parent.winfo_width()
                - self.WIDTH
            ) // 2
        )

        y = (
            self.parent.winfo_rooty() +
            (
                self.parent.winfo_height()
                - self.HEIGHT
            ) // 2
        )

        self.geometry(
            f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}"
        )

    def set_summary(
        self,
        folders,
        files,
        total_size
    ):

        self.summary_label.configure(
            text=(
                f"{folders} folders, "
                f"{files} files    "
                f"Total: {total_size}"
            )
        )

    def clear_items(self):

        for widget in self.list_frame.winfo_children():

            widget.destroy()

        self.item_status_labels.clear()
        self.folder_items.clear()

    def add_item(
        self,
        name,
        item_type,
        size,
        item_key=None
    ):

        if item_key is None:
            item_key = name

        row = tk.Frame(
            self.list_frame
        )

        if item_type == "folder":

            icon = "📁"

        else:

            icon = "📄"

        icon_label = tk.Label(
            row,
            text=icon,
            font=("Segoe UI", 11)
        )

        name_label = tk.Label(
            row,
            text=name,
            anchor="w"
        )

        size_label = tk.Label(
            row,
            text=size,
            width=12,
            anchor="e"
        )

        status_label = tk.Label(
            row,
            text="⏳",
            width=4
        )

        icon_label.pack(
            side="left"
        )

        name_label.pack(
            side="left",
            fill="x",
            expand=True,
            padx=8
        )

        size_label.pack(
            side="left"
        )

        status_label.pack(
            side="left"
        )

        row.pack(
            fill="x",
            pady=3
        )

        self.item_status_labels[item_key] = status_label

        if item_type == "folder":

            folder_files = int(
                str(size).split()[0]
            )

            self.folder_items[item_key] = {
                "files": folder_files,
                "completed": 0,
                "failed": 0
            }

        return status_label

    def set_progress(self, value):

        value = max(
            0,
            min(
                100,
                value
            )
        )

        self.progress.set(
            value
        )

        self.progress_label.configure(
            text=f"Progress: {value:.0f}%"
        )

    def set_item_status(
        self,
        status_label,
        status
    ):

        icons = {
            "waiting": "⏳",
            "transferring": "🔄",
            "transferred": "✅",
            "failed": "❌"
        }

        status_label.configure(
            text=icons.get(
                status,
                "⏳"
            )
        )

    def set_item_status_by_key(
        self,
        item_key,
        status
    ):

        status_label = (
            self.item_status_labels.get(item_key)
        )

        if status_label is None:
            return

        self.set_item_status(
            status_label,
            status
        )

    def set_folder_file_status(
        self,
        relative_path,
        status
    ):

        relative_path = str(
            relative_path
        )

        parts = relative_path.replace(
            "\\",
            "/"
        ).split("/")

        # Fayl root-da yerləşirsə,
        # folder statusuna təsir etmir.
        if len(parts) <= 1:
            return

        folder_key = (
            f"folder:{parts[0]}"
        )

        folder_data = (
            self.folder_items.get(
                folder_key
            )
        )

        if folder_data is None:
            return

        if status == "transferred":

            folder_data["completed"] += 1

        elif status == "failed":

            folder_data["failed"] += 1

        total = folder_data["files"]

        completed = folder_data["completed"]
        failed = folder_data["failed"]

        if failed > 0:

            folder_status = "failed"

        elif completed >= total:

            folder_status = "transferred"

        else:

            folder_status = "transferring"

        self.set_item_status_by_key(
            folder_key,
            folder_status
        )

    def set_transfer_finished(
        self,
        failed_files=0
    ):

        if failed_files > 0:

            self.progress_label.configure(
                text=(
                    f"Transfer finished "
                    f"with {failed_files} failed file(s)"
                )
            )

        else:

            self.progress.set(
                100
            )

            self.progress_label.configure(
                text="Transfer completed successfully"
            )