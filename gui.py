import customtkinter as ctk
import threading
from main import run_assistant, stop_assistant, handle_query
from PIL import Image

# ---------------- APP CONFIG ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Pixel AI Assistant")
app.geometry("760x720")
app.resizable(False, False)

# ---------------- HEADER ----------------
header = ctk.CTkFrame(app, height=60)
header.pack(fill="x", padx=10, pady=(10, 5))

logo = ctk.CTkImage(
    light_image=Image.open("pixel_logo.png"),
    dark_image=Image.open("pixel_logo.png"),
    size=(42, 42)
)

ctk.CTkLabel(header, image=logo, text="").pack(side="left", padx=10)

ctk.CTkLabel(
    header,
    text="Pixel AI Assistant",
    font=("Segoe UI", 22, "bold")
).pack(side="left")

status_label = ctk.CTkLabel(
    header,
    text="● Idle",
    font=("Segoe UI", 14),
    text_color="orange"
)
status_label.pack(side="right", padx=15)

# ---------------- CHAT AREA ----------------
chat_frame = ctk.CTkScrollableFrame(
    app,
    corner_radius=12,
    fg_color="#1e1e1e"
)
chat_frame.pack(fill="both", expand=True, padx=12, pady=8)

def add_message(text, sender="pixel"):
    is_user = sender == "user"
    is_code = (
        "```" in text or
        text.strip().startswith("<") or
        len(text) > 300
    )

    row = ctk.CTkFrame(chat_frame, fg_color="transparent")
    row.pack(fill="x", padx=10, pady=6)

    if is_code:
        bubble = ctk.CTkFrame(
            row,
            fg_color="#2b2b2b",
            corner_radius=16
        )
        bubble.pack(anchor="e" if is_user else "w")

        preview_height = 140

        textbox = ctk.CTkTextbox(
            bubble,
            width=520,
            height=preview_height,
            wrap="word",
            font=("Consolas", 13),
            fg_color="transparent",
            border_width=0
        )
        textbox.insert("1.0", text)
        textbox.configure(state="disabled")
        textbox.pack(padx=12, pady=(10, 4))

        def toggle():
            if textbox.cget("height") == preview_height:
                textbox.configure(height=300)
                toggle_btn.configure(text="Collapse")
            else:
                textbox.configure(height=preview_height)
                toggle_btn.configure(text="Expand")

        toggle_btn = ctk.CTkButton(
            bubble,
            text="Expand",
            width=80,
            height=26,
            font=("Segoe UI", 12),
            fg_color="#3a3a3a",
            hover_color="#4a4a4a",
            command=toggle
        )
        toggle_btn.pack(anchor="e", padx=10, pady=(0, 8))

    else:
        bubble = ctk.CTkLabel(
            row,
            text=text,
            wraplength=520,
            justify="left",
            anchor="w",
            font=("Segoe UI", 14),
            corner_radius=16,
            padx=14,
            pady=10,
            fg_color="#1f6aa5" if is_user else "#2b2b2b"
        )
        bubble.pack(anchor="e" if is_user else "w")

    chat_frame.update_idletasks()
    chat_frame._parent_canvas.yview_moveto(1.0)

# Welcome
add_message("Hi! I am Pixel 🤖\nHow can I help you today?")

# ---------------- INPUT AREA ----------------
input_frame = ctk.CTkFrame(app)
input_frame.pack(fill="x", padx=12, pady=(6, 4))

user_entry = ctk.CTkEntry(
    input_frame,
    placeholder_text="Type your message...",
    font=("Segoe UI", 14)
)
user_entry.pack(side="left", fill="x", expand=True, padx=(6, 8))

def send_message():
    query = user_entry.get().strip()
    if not query:
        return

    add_message(query, "user")
    user_entry.delete(0, "end")

    status_label.configure(text="● Thinking", text_color="yellow")

    def process():
        response = handle_query(query)
        add_message(response, "pixel")
        status_label.configure(text="● Idle", text_color="orange")

    threading.Thread(target=process, daemon=True).start()

user_entry.bind("<Return>", lambda e: send_message())

ctk.CTkButton(
    input_frame,
    text="Send",
    width=90,
    command=send_message
).pack(side="right", padx=6)

# ---------------- CONTROLS ----------------
controls = ctk.CTkFrame(app)
controls.pack(pady=(6, 12))

def start_voice():
    status_label.configure(text="● Listening", text_color="green")
    add_message("🎤 Listening... Say 'Hey Pixel'")

    threading.Thread(
        target=run_assistant,
        args=(lambda msg: add_message(msg.replace("Pixel:", ""), "pixel"),),
        daemon=True
    ).start()

def stop_voice():
    stop_assistant()
    status_label.configure(text="● Stopped", text_color="red")
    add_message("Assistant stopped.")

def clear_chat():
    for w in chat_frame.winfo_children():
        w.destroy()
    add_message("Chat cleared. How can I help?")

ctk.CTkButton(controls, text="🎤 Start", width=160, command=start_voice).grid(row=0, column=0, padx=8)
ctk.CTkButton(controls, text="⏹ Stop", width=120, fg_color="#c0392b", command=stop_voice).grid(row=0, column=1, padx=8)
ctk.CTkButton(controls, text="🧹 Clear", width=140, fg_color="#566573", command=clear_chat).grid(row=0, column=2, padx=8)

app.mainloop()
