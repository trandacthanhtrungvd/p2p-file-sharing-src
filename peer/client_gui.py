import config
import threading
import customtkinter
from tkinter import StringVar
from tkinterdnd2 import TkinterDnD, DND_FILES
from client import start_server
from fetch import start_fetch
from publish import publish

# Settings
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# Tips for file entry
# Reference: https://stackoverflow.com/questions/75526264/using-drag-and-drop-files-or-file-picker-with-customtkinter
class Tk(customtkinter.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

# Callbacks

# Some support functions

# Frames
class CentralizedServerFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.server_entry = customtkinter.CTkEntry(self, width=229, height=40, placeholder_text="Input Server's Address...")
        self.server_entry.grid(row=0, column=0, padx=8)

        self.server_button = customtkinter.CTkButton(self, text="Change", width=103, height=32, command=self.server_button_callback)
        self.server_button.grid(row=0, column=1)
    
    def server_button_callback(self):
        config.SERVER = self.server_entry.get()



class PublishFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=0)

        self.lname_label = customtkinter.CTkLabel(self, text="Local File")
        self.lname_label.grid(row=0, padx=8, pady=(4, 0), sticky="w")

        self.lname_entry = customtkinter.CTkEntry(self, width=340, height=40, placeholder_text="Input Local File...")
        self.lname_entry.grid(row=1, padx=8, pady=(0, 24), sticky="w")
        self.lname_entry.drop_target_register(DND_FILES)
        self.lname_entry.dnd_bind("<<Drop>>", self.handle_file_drop)

        self.fname_label = customtkinter.CTkLabel(self, text="File Name")
        self.fname_label.grid(row=2, padx=8, sticky="w")

        self.fname_entry = customtkinter.CTkEntry(self, width=340, height=40, placeholder_text="Input File Name...")
        self.fname_entry.grid(row=3, padx=8, pady=(0, 24), sticky="w")

        self.publish_button = customtkinter.CTkButton(self, text="Publish", width=103, height=32, command=self.publish_button_callback)
        self.publish_button.grid(row=4, padx=8, pady=(0, 16), sticky="w")
    
    def publish_button_callback(self):
        fname = self.fname_entry.get()
        lname = self.lname_entry.get()
        threading.Thread(target=publish, args=(config.SERVER, lname, fname, )).start()

    def handle_file_drop(self, event):
        self.lname_entry.delete(0, "end")
        self.lname_entry.insert("end", event.data[1:-1])

class FetchFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=356, height=243)
        
        self.fname_label = customtkinter.CTkLabel(self, text="File Name")
        self.fname_label.grid(row=0, padx=8, pady=(4, 0), sticky="w")

        self.fname_entry = customtkinter.CTkEntry(self, width=340, height=40, placeholder_text="Input File Name...")
        self.fname_entry.grid(row=1, padx=8, pady=(0, 24), sticky="we")

        self.fetch_button = customtkinter.CTkButton(self, text="Fetch", width=103, height=32, command=self.fetch_button_callback)
        self.fetch_button.grid(row=2, padx=8, sticky="w")

    def fetch_button_callback(self):
        fname = self.fname_entry.get()
        threading.Thread(target=start_fetch, args=(config.SERVER, fname, )).start()


# Main App
class App(Tk):
    def __init__(self):
        super().__init__()

        # Some metadata
        self.title("P2P File Sharing System - Client")
        self.geometry("800x460")
        
        # Grid configurations
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # UI elements
        start_button = customtkinter.CTkButton(self, text="Start Sharing", width=103, height=32, command=self.start_button_callback)
        start_button.grid(row=0, column=0, columnspan=2, padx=(32, 0), pady=32, sticky="w")

        # Place frames inside window
        server_frame = CentralizedServerFrame(self)
        server_frame.grid(row=0, column=1, padx=(12, 32), pady=32, sticky="news")

        publish_frame = PublishFrame(self)
        publish_frame.grid(row=1, column=0, padx=(32, 12), pady=(0, 32), sticky="news")

        fetch_frame = FetchFrame(self)
        fetch_frame.grid(row=1, column=1, padx=(12, 32), pady=(0, 32), sticky="news")
    
    def start_button_callback(self):
        threading.Thread(target=start_server).start()

app = App()
app.mainloop()