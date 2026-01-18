import customtkinter as ctk
import threading
from main import run_assistant, stop_assistant, handle_query
from PIL import Image

# ---------------- APP CONFIG ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Pixel AI Assistant")
app.geometry("720x680")
app.resizable(False, False)

# ---------------- LOGO ----------------
logo_image = ctk.CTkImage(
    light_image=Image.open("pixel_logo.png"),
    dark_image=Image.open("pixel_logo.png"),
    size=(50, 50)
)

# ---------------- HEADER ----------------
header = ctk.CTkFrame(app)
header.pack(fill="x", padx=10, pady=(10, 5))

logo_label = ctk.CTkLabel(header, image=logo_image, text="")
logo_label.pack(side="left", padx=(10, 6))

title = ctk.CTkLabel(
    header,
    text="Pixel AI Desktop Assistant",
    font=("Segoe UI", 22, "bold")
)
title.pack(side="left")

status_label = ctk.CTkLabel(
    header,
    text="● Idle",
    font=("Segoe UI", 14),
    text_color="orange"
)
status_label.pack(side="right", padx=10)

# ---------------- CHAT AREA ----------------
chat_container = ctk.CTkScrollableFrame(
    app,
    fg_color="#1E1E1E",
    corner_radius=10
)
chat_container.pack(fill="both", expand=True, padx=12, pady=8)

def add_message(text, sender="pixel"):
    row = ctk.CTkFrame(chat_container, fg_color="transparent")
    row.pack(fill="x", pady=6)

    if sender == "user":
        bubble = ctk.CTkLabel(
            row,
            text=text,
            wraplength=420,
            justify="left",
            font=("Segoe UI", 14),
            fg_color="#1F6AA5",
            text_color="white",
            corner_radius=18,
            padx=14,
            pady=10
        )
        bubble.pack(anchor="e", padx=12)
    else:
        bubble = ctk.CTkLabel(
            row,
            text=text,
            wraplength=420,
            justify="left",
            font=("Segoe UI", 14),
            fg_color="#2C2C2C",
            text_color="white",
            corner_radius=18,
            padx=14,
            pady=10
        )
        bubble.pack(anchor="w", padx=12)
        
    chat_container.update_idletasks()
    chat_container._parent_canvas.yview_moveto(1.0)
# Welcome message (IMPORTANT)
add_message("Hi! I am Pixel 🤖\nHow can I help you today?", "pixel")

# ---------------- TEXT INPUT ----------------
input_frame = ctk.CTkFrame(app)
input_frame.pack(fill="x", padx=12, pady=(6, 4))

user_input = ctk.CTkEntry(
    input_frame,
    placeholder_text="Type a message...",
    font=("Segoe UI", 14)
)
user_input.pack(side="left", fill="x", expand=True, padx=6)

def send_text():
    query = user_input.get().strip()
    if not query:
        return

    add_message(query, "user")
    user_input.delete(0, "end")

    status_label.configure(text="● Thinking", text_color="yellow")
    app.update()

    response = handle_query(query)
    add_message(response, "pixel")

    status_label.configure(text="● Idle", text_color="orange")

user_input.bind("<Return>", lambda e: send_text())

send_btn = ctk.CTkButton(
    input_frame,
    text="Send",
    width=90,
    command=send_text
)
send_btn.pack(side="right", padx=6)

# ---------------- CONTROL BUTTONS ----------------
btn_frame = ctk.CTkFrame(app)
btn_frame.pack(pady=(6, 12))

def start_voice():
    start_btn.configure(state="disabled")
    status_label.configure(text="● Listening", text_color="green")
    add_message("Listening... Speak now.", "pixel")

    threading.Thread(
        target=run_assistant,
        args=(lambda msg: add_message(msg.replace("Pixel: ", ""), "pixel"),),
        daemon=True
    ).start()

def stop_voice():
    stop_assistant()
    start_btn.configure(state="normal")
    status_label.configure(text="● Stopped", text_color="red")
    add_message("Assistant stopped.", "pixel")

def clear_chat():
    for w in chat_container.winfo_children():
        w.destroy()
    add_message("Chat cleared. How can I help?", "pixel")

start_btn = ctk.CTkButton(
    btn_frame,
    text="🎤 Turn on mic",
    width=180,
    height=42,
    font=("Segoe UI", 14),
    command=start_voice
)
start_btn.grid(row=0, column=0, padx=8)

stop_btn = ctk.CTkButton(
    btn_frame,
    text="⏹ Stop",
    width=120,
    height=42,
    font=("Segoe UI", 14),
    fg_color="#C0392B",
    hover_color="#A93226",
    command=stop_voice
)
stop_btn.grid(row=0, column=1, padx=8)

clear_btn = ctk.CTkButton(
    btn_frame,
    text="🧹 Clear Chat",
    width=140,
    height=42,
    font=("Segoe UI", 14),
    fg_color="#5D6D7E",
    hover_color="#566573",
    command=clear_chat
)
clear_btn.grid(row=0, column=2, padx=8)

app.mainloop()
