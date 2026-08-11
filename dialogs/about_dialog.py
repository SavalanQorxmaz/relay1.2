import tkinter as tk


class AboutDialog(tk.Toplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title("About")

        self.resizable(False, False)

        self.geometry("420x220")

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
        ).pack(pady=(15,5))

        tk.Label(
            self,
            text="Simple LAN File Transfer"
        ).pack()

        tk.Label(
            self,
            text="\nDeveloper\nSavalan Qorxmaz"
        ).pack()

        tk.Label(
            self,
            text="\nAI Assisted Development\nOpenAI ChatGPT",
            fg="#666666"
        ).pack()

        tk.Button(
            self,
            text="Close",
            command=self.destroy
        ).pack(pady=15)