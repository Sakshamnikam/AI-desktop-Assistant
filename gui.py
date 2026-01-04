import customtkinter as ctk
import threading
from main import run_assistant, stop_assistant, handle_query

# ---------------- CONFIG ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Pixel AI Assistant")
app.geometry("620x620")
app.resizable(False, False)

# ---------------- HEADER ----------------
header = ctk.CTkFrame(app, fg_color="transparent")
header.pack(pady=15)

title = ctk.CTkLabel(
    header,
    text="🤖 Pixel AI Assistant",
    font=("Segoe UI", 26, "bold")
)
title.pack()

status_label = ctk.CTkLabel(
    header,
    text="🔴 Stopped",
    font=("Segoe UI", 14),
    text_color="red"
)
status_label.pack(pady=5)

# ---------------- CHAT BOX ----------------
chat_box = ctk.CTkTextbox(
    app,
    width=560,
    height=360,
    font=("Segoe UI", 14),
    wrap="word"
)
chat_box.pack(pady=10)
chat_box.configure(state="disabled")

def log_to_gui(message, sender="pixel"):
    chat_box.configure(state="normal")

    if sender == "user":
        chat_box.insert("end", f"\n🧑 You: {message}\n")
    else:
        chat_box.insert("end", f"\n🤖 Pixel: {message}\n")

    chat_box.see("end")
    chat_box.configure(state="disabled")

# ---------------- TEXT INPUT ----------------
input_frame = ctk.CTkFrame(app, fg_color="transparent")
input_frame.pack(pady=10)

text_input = ctk.CTkEntry(
    input_frame,
    width=420,
    height=40,
    placeholder_text="Type a message (AI fallback)...",
    font=("Segoe UI", 14)
)
text_input.grid(row=0, column=0, padx=10)

def send_text_query(event=None):
    query = text_input.get().strip()
    if not query:
        return

    log_to_gui(query, sender="user")
    text_input.delete(0, "end")

    response = handle_query(query)
    log_to_gui(response, sender="pixel")

text_input.bind("<Return>", send_text_query)

send_btn = ctk.CTkButton(
    input_frame,
    text="Send",
    width=100,
    height=40,
    command=send_text_query
)
send_btn.grid(row=0, column=1)

# ---------------- BUTTONS ----------------
btn_frame = ctk.CTkFrame(app, fg_color="transparent")
btn_frame.pack(pady=15)

def start_assistant_gui():
    start_btn.configure(state="disabled")
    status_label.configure(text="🟢 Listening", text_color="green")
    log_to_gui("Assistant started. Speak now...")

    threading.Thread(
        target=run_assistant,
        args=(lambda msg: log_to_gui(msg.replace("Pixel: ", ""), "pixel"),),
        daemon=True
    ).start()

def stop_assistant_gui():
    stop_assistant()
    start_btn.configure(state="normal")
    status_label.configure(text="🔴 Stopped", text_color="red")
    log_to_gui("Assistant stopped.")

def clear_chat():
    chat_box.configure(state="normal")
    chat_box.delete("1.0", "end")
    chat_box.configure(state="disabled")

start_btn = ctk.CTkButton(
    btn_frame,
    text="🎤 Start Listening",
    width=180,
    height=45,
    font=("Segoe UI", 15),
    command=start_assistant_gui
)
start_btn.grid(row=0, column=0, padx=10)

stop_btn = ctk.CTkButton(
    btn_frame,
    text="⏹ Stop",
    width=120,
    height=45,
    font=("Segoe UI", 15),
    fg_color="#C0392B",
    hover_color="#A93226",
    command=stop_assistant_gui
)
stop_btn.grid(row=0, column=1, padx=10)

clear_btn = ctk.CTkButton(
    btn_frame,
    text="🧹 Clear Chat",
    width=140,
    height=45,
    font=("Segoe UI", 15),
    fg_color="#5D6D7E",
    hover_color="#566573",
    command=clear_chat
)
clear_btn.grid(row=0, column=2, padx=10)

app.mainloop()
