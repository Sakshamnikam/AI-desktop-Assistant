import customtkinter as ctk
import threading
from main import run_assistant, stop_assistant, handle_query
from PIL import Image
import os
import sys


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores files there
        base_path = sys._MEIPASS
    except Exception:
        # Normal Python execution
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
# ---------------- STATE ----------------
assistant_listening = False

# ---------------- SAFE UI HELPERS ----------------
def set_status(text, color):
    app.after(0, lambda: status_label.configure(text=text, text_color=color))

# ---------------- APP CONFIG ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Pixel AI Assistant")
app.geometry("760x720")
app.resizable(False, False)
app.configure(fg_color="#0f1115")

# ---------------- HEADER ----------------
header = ctk.CTkFrame(app, height=52, fg_color="#0f1115")
header.pack(fill="x")

logo = ctk.CTkImage(
    light_image=Image.open(resource_path("pixel_logo.png")),
    dark_image=Image.open(resource_path("pixel_logo.png")),
    size=(36, 36)
)

ctk.CTkLabel(header, image=logo, text="").pack(side="left", padx=(12, 8))

ctk.CTkLabel(
    header,
    text="Pixel AI Assistant",
    font=("Segoe UI Semibold", 18)
).pack(side="left")

status_label = ctk.CTkLabel(
    header,
    text="● Idle",
    font=("Segoe UI", 12),
    text_color="#facc15"
)
status_label.pack(side="right", padx=14)

# ---------------- CHAT AREA ----------------
chat_frame = ctk.CTkScrollableFrame(
    app,
    fg_color="#161a20",
    corner_radius=12
)
chat_frame.pack(fill="both", expand=True, padx=12, pady=(10, 8))

def add_message(text, sender="pixel"):
    is_user = sender == "user"
    is_code = "```" in text or len(text) > 300

    # Full-width row
    row = ctk.CTkFrame(chat_frame, fg_color="transparent")
    row.pack(fill="x", padx=10, pady=6)

    # Alignment container (content-width only)
    align = ctk.CTkFrame(row, fg_color="transparent")
    align.pack(
        anchor="e" if is_user else "w",
        padx=(20, 0) if is_user else (0, 20)
    )

    if is_code:
        bubble = ctk.CTkFrame(
            align,
            fg_color="#1e293b",
            corner_radius=14
        )
        bubble.pack()

        preview_height = 140
        textbox = ctk.CTkTextbox(
            bubble,
            width=480,
            height=preview_height,
            wrap="none",
            font=("Consolas", 13),
            fg_color="transparent",
            border_width=0
        )
        textbox.insert("1.0", text)
        textbox.configure(state="disabled")
        textbox.pack(padx=12, pady=(10, 4))

        def toggle():
            if textbox.cget("height") == preview_height:
                textbox.configure(height=320)
                toggle_btn.configure(text="Collapse")
            else:
                textbox.configure(height=preview_height)
                toggle_btn.configure(text="Expand")

        toggle_btn = ctk.CTkButton(
            bubble,
            text="Expand",
            width=80,
            height=26,
            font=("Segoe UI", 11),
            fg_color="#334155",
            hover_color="#475569",
            command=toggle
        )
        toggle_btn.pack(anchor="e", padx=10, pady=(0, 8))

    else:
        bubble = ctk.CTkLabel(
            align,   # ✅ CORRECT PARENT
            text=text,
            wraplength=480,
            justify="left",
            anchor="w",
            font=("Segoe UI", 14),
            corner_radius=16,
            padx=14,
            pady=10,
            fg_color="#2563eb" if is_user else "#23272f"
        )
        bubble.pack()

    chat_frame.update_idletasks()
    chat_frame._parent_canvas.yview_moveto(1.0)


add_message("Hi! I am Pixel 🤖\nHow can I help you today?")

# ---------------- INPUT AREA ----------------
input_frame = ctk.CTkFrame(app, fg_color="#0f1115")
input_frame.pack(fill="x", padx=12, pady=(4, 6))

user_entry = ctk.CTkEntry(
    input_frame,
    placeholder_text="Type your message...",
    height=40,
    font=("Segoe UI", 14),
    fg_color="#161a20",
    border_color="#2a2f3a"
)
user_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

def send_message():
    query = user_entry.get().strip()
    if not query:
        return

    add_message(query, "user")
    user_entry.delete(0, "end")
    user_entry.focus()

    set_status("● Thinking", "#38bdf8")

    def process():
        response = handle_query(query)
        app.after(0, lambda: add_message(response, "pixel"))
        if not assistant_listening:
            set_status("● Idle", "#facc15")

    threading.Thread(target=process, daemon=True).start()

user_entry.bind("<Return>", lambda e: send_message())

ctk.CTkButton(
    input_frame,
    text="Send",
    width=90,
    height=40,
    font=("Segoe UI Semibold", 13),
    fg_color="#3b82f6",
    hover_color="#2563eb",
    command=send_message
).pack(side="right")

# ---------------- VOICE CONTROLS ----------------
controls = ctk.CTkFrame(app, fg_color="#0f1115")
controls.pack(fill="x", pady=(0, 10))

def start_voice():
    global assistant_listening
    assistant_listening = True
    set_status("● Listening", "green")

    threading.Thread(
        target=run_assistant,
        args=(lambda msg: app.after(0, lambda: add_message(msg.replace("Pixel:", ""), "pixel")),),
        daemon=True
    ).start()

def stop_voice():
    global assistant_listening
    assistant_listening = False
    stop_assistant()
    set_status("● Stopped", "red")
    add_message("Assistant stopped.")

def clear_chat():
    for w in chat_frame.winfo_children():
        w.destroy()
    add_message("Chat cleared. How can I help?")

ctk.CTkButton(controls, text="🎤 Start", width=120, command=start_voice).pack(side="left", padx=6)
ctk.CTkButton(controls, text="⏹ Stop", width=100, fg_color="#dc2626", command=stop_voice).pack(side="left", padx=6)
ctk.CTkButton(controls, text="🧹 Clear", width=110, fg_color="#334155", command=clear_chat).pack(side="left", padx=6)

app.mainloop()
