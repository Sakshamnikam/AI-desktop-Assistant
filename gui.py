import customtkinter as ctk
import threading
from main import run_assistant, stop_assistant

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Pixel AI Assistant")
app.geometry("550x480")
app.resizable(False, False)

# ---------------- HEADER ----------------
title = ctk.CTkLabel(app, text="Pixel AI Assistant", font=("Segoe UI", 24, "bold"))
title.pack(pady=(20, 5))

status_label = ctk.CTkLabel(app, text="Status: Idle", font=("Segoe UI", 14), text_color="orange")
status_label.pack(pady=5)

# ---------------- CHAT BOX ----------------
chat_box = ctk.CTkTextbox(app, width=500, height=280, font=("Segoe UI", 13))
chat_box.pack(pady=15)
chat_box.configure(state="disabled")

def log_to_gui(message):
    chat_box.configure(state="normal")
    chat_box.insert("end", message + "\n\n")
    chat_box.see("end")
    chat_box.configure(state="disabled")
    
# ---------------- BUTTON ACTIONS ----------------
def start_assistant_gui():
    status_label.configure(text="Status: Listening", text_color="green")
    log_to_gui("🎤 Assistant started...\n")
    threading.Thread(
        target=run_assistant,
        args=(log_to_gui,),
        daemon=True
    ).start()

def stop_assistant_gui():
    stop_assistant()
    status_label.configure(text="Status: Stopped", text_color="red")
    log_to_gui("⏹ Assistant stopped")

# ---------------- BUTTONS ----------------
btn_frame = ctk.CTkFrame(app, fg_color="transparent")
btn_frame.pack(pady=10)

ctk.CTkButton(
    btn_frame,
    text="🎤 Start Listening",
    width=180,
    height=45,
    font=("Segoe UI", 15),
    command=start_assistant_gui
).grid(row=0, column=0, padx=10)

ctk.CTkButton(
    btn_frame,
    text="⏹ Stop",
    width=120,
    height=45,
    font=("Segoe UI", 15),
    fg_color="#C0392B",
    hover_color="#A93226",
    command=stop_assistant_gui
).grid(row=0, column=1, padx=10)

app.mainloop()
