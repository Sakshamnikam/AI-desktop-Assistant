import customtkinter as ctk
import threading
from main import run_assistant, stop_assistant

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Pixel AI Assistant")
app.geometry("500x350")

title = ctk.CTkLabel(app, text="Pixel AI Assistant", font=("Arial", 22))
title.pack(pady=20)

status = ctk.CTkLabel(app, text="Status: Idle", font=("Arial", 14))
status.pack(pady=10)

def start():
    status.configure(text="Status: Listening...")
    threading.Thread(target=run_assistant, daemon=True).start()

def stop():
    stop_assistant()
    status.configure(text="Status: Stopped")

start_btn = ctk.CTkButton(app, text="🎤 Start Assistant", command=start)
start_btn.pack(pady=10)

stop_btn = ctk.CTkButton(app, text="⏹ Stop Assistant", fg_color="red", command=stop)
stop_btn.pack(pady=5)

app.mainloop()
