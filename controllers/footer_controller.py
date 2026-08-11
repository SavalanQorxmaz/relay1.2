"""
Relay 1.2

Footer Controller
"""

import os
from tkinter import filedialog, messagebox
from pathlib import Path
from dialogs.about_dialog import AboutDialog
from dialogs.help_dialog import HelpDialog
from services.firewall_service import FirewallService

class FooterController:

    def __init__(self, footer_panel):

        self.footer_panel = footer_panel

        self.initialize()

    def initialize(self):

        self.footer_panel.firewall_button.configure(
            command=self.export_firewall_tool
        )

    def show_about(self):

        AboutDialog(
            self.footer_panel.winfo_toplevel()
        )

    def show_help(self):

        HelpDialog(
            self.footer_panel.winfo_toplevel()
        )
        
    def export_firewall_tool(self):

        desktop = Path(
            os.environ["USERPROFILE"]
        ) / "Desktop"

        destination = filedialog.asksaveasfilename(

            initialdir=desktop,

            defaultextension=".cmd",

            initialfile="relay_firewall.cmd",

            filetypes=[
                ("Command File", "*.cmd")
            ]
        )

        if not destination:
            return

        try:

            with open(
                destination,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    FirewallService.generate_batch()
                )

            messagebox.showinfo(
                "Relay",
                "Firewall Tool has been exported.\n\nRun the file as Administrator."
            )

        except Exception as e:

            messagebox.showerror(
                "Relay",
                str(e)
            )