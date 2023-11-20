import threading
import customtkinter
from centralized_server import *

# Settings
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("P2P File Sharing System - Centralized Server")
        self.geometry("800x460")

        # Adding UI elements
        button = customtkinter.CTkButton(self, text="Start Server", command=start_server)
        button.grid(row=0, column=0, padx=32, pady=20)

        # Discover
        # discover_frame = customtkinter.CTkFrame(master=app)
        # discover_frame.pack(fill="both")

        # Ping
        # ping_frame = customtkinter.CTkFrame(master=app)
        # ping_frame.pack(fill="both")

app = App()
app.mainloop()