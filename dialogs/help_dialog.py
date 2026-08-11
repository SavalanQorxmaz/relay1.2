

import tkinter as tk



class HelpDialog(tk.Toplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title("Help")

        self.resizable(False, False)

        self.geometry("460x280")

        self.transient(parent)
        self.grab_set()

        self.update_idletasks()

        width = self.winfo_width()
        height = self.winfo_height()

        x = parent.winfo_rootx() + (parent.winfo_width() - width) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")

        self.focus_force()
        tk.Label(
            self,
            text="Relay 1.2",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=(15, 8))

        help_text = (
            "1. Configure the Windows Firewall.\n\n"
            "2. Select a Receive Folder.\n\n"
            "3. Share your Relay ID.\n\n"
            "4. Connect to another Relay.\n\n"
            "5. Send or receive files.\n\n"
            "If the firewall cannot be configured automatically,\n"
            "use 'Firewall Tool' to export the CMD file and run it\n"
            "as Administrator."
        )

        tk.Label(
            self,
            text=help_text,
            justify="left",
            anchor="w"
        ).pack(
            padx=20,
            fill="x"
        )

        tk.Button(
            self,
            text="Close",
            command=self.destroy
        ).pack(pady=15)