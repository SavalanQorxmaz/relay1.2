import tkinter as tk


class ConnectionPopup(tk.Toplevel):

    WIDTH = 420
    HEIGHT = 180

    def __init__(self, master):

        super().__init__(master)

        self.on_accept = None
        self.on_reject = None
        self.on_cancel = None

        self.withdraw()

        self.title("Connection")

        self.resizable(False, False)

        self.transient(master)

        self.protocol(
            "WM_DELETE_WINDOW",
            self.cancel_clicked
        )

        self.create_layout()
        self.create_widgets()
        self.place_widgets()

    # -------------------------------------------------

    def create_layout(self):

        self.content = tk.Frame(self)

        self.content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

    # -------------------------------------------------

    def create_widgets(self):

        self.title_label = tk.Label(
            self.content,
            text="",
            font=("Segoe UI", 12, "bold")
        )

        self.relay_id_label = tk.Label(
            self.content,
            text="",
            font=("Segoe UI", 10)
        )

        self.status_label = tk.Label(
            self.content,
            text="",
            font=("Segoe UI", 10)
        )

        self.button_frame = tk.Frame(
            self.content
        )

        self.accept_button = tk.Button(
            self.button_frame,
            text="Accept",
            width=10,
            command=self.accept_clicked
        )

        self.reject_button = tk.Button(
            self.button_frame,
            text="Reject",
            width=10,
            command=self.reject_clicked
        )

        self.cancel_button = tk.Button(
            self.button_frame,
            text="Cancel",
            width=10,
            command=self.cancel_clicked
        )

    # -------------------------------------------------

    def place_widgets(self):

        self.title_label.pack(
            pady=(0, 10)
        )

        self.relay_id_label.pack(
            pady=5
        )

        self.status_label.pack(
            pady=(0, 20)
        )

        self.button_frame.pack()

    # -------------------------------------------------
    # Callback
    # -------------------------------------------------

    def set_accept_callback(
        self,
        callback
    ):

        self.on_accept = callback

    def set_reject_callback(
        self,
        callback
    ):

        self.on_reject = callback

    def set_cancel_callback(
        self,
        callback
    ):

        self.on_cancel = callback

    # -------------------------------------------------
    # Events
    # -------------------------------------------------

    def accept_clicked(self):

        self.hide()

        if self.on_accept:

            self.on_accept()

    def reject_clicked(self):

        self.hide()

        if self.on_reject:

            self.on_reject()

    def cancel_clicked(self):

        self.hide()

        if self.on_cancel:

            self.on_cancel()

    # -------------------------------------------------
    # States
    # -------------------------------------------------

    def show_waiting(
        self,
        relay_id
    ):

        self.title_label.configure(
            text="Connecting..."
        )

        self.relay_id_label.configure(
            text=f"Relay ID : {relay_id}"
        )

        self.status_label.configure(
            text="Waiting for response..."
        )

        for widget in self.button_frame.winfo_children():
            widget.pack_forget()

        self.cancel_button.pack()

        self.show()

    def show_incoming(
        self,
        relay_id
    ):

        self.title_label.configure(
            text="Incoming Connection"
        )

        self.relay_id_label.configure(
            text=f"Relay ID : {relay_id}"
        )

        self.status_label.configure(
            text="Accept this connection?"
        )

        for widget in self.button_frame.winfo_children():
            widget.pack_forget()

        self.accept_button.pack(
            side="left",
            padx=5
        )

        self.reject_button.pack(
            side="left",
            padx=5
        )

        self.show()

    # -------------------------------------------------

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

    # -------------------------------------------------

    def center(self):

        self.update_idletasks()

        x = (
            self.master.winfo_rootx() +
            (self.master.winfo_width() - self.WIDTH) // 2
        )

        y = (
            self.master.winfo_rooty() +
            (self.master.winfo_height() - self.HEIGHT) // 2
        )

        self.geometry(
            f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}"
        )