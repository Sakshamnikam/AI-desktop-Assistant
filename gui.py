# =========================
# PIXEL UI THEME
# =========================

COLORS = {
    "bg": "#050816",
    "surface": "#111827",
    "surface2": "#1E293B",

    "accent": "#00D9FF",
    "accent_hover": "#00B8D9",

    "success": "#22C55E",
    "warning": "#FACC15",
    "error": "#EF4444",

    "text": "#F8FAFC",
    "text_secondary": "#94A3B8",

    "user_bubble": "#00D9FF",
    "assistant_bubble": "#1E293B",

    "input": "#0F172A"
}

FONTS = {
    "title": ("Segoe UI Semibold", 22),
    "subtitle": ("Segoe UI", 12),
    "chat": ("Segoe UI", 14),
    "status": ("Segoe UI", 11),
    "button": ("Segoe UI Semibold", 13)
}

import customtkinter as ctk
import threading
from main import run_assistant, stop_assistant, handle_query
from datetime import datetime
from PIL import Image
import os

# ---------------- APP CONFIG ----------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Pixel AI Assistant")
app.geometry("900x760")
app.minsize(850, 700)
app.configure(fg_color=COLORS["bg"])

# Window icon
if os.path.exists("pixel_logo.ico"):
    app.iconbitmap("pixel_logo.ico")

assistant_listening = False
glow_job = None
glow_intensity = 100
glow_direction = 1

# ---------------- HEADER ----------------
header = ctk.CTkFrame(app, height=60, fg_color=COLORS["bg"])
header.pack(fill="x")

left = ctk.CTkFrame(header, fg_color="transparent")
left.pack(side="left", padx=14)

# -------- LOGO --------
if os.path.exists("pixel_logo.png"):
    logo_image = ctk.CTkImage(
        light_image=Image.open("pixel_logo.png"),
        dark_image=Image.open("pixel_logo.png"),
        size=(32, 32)
    )
    ctk.CTkLabel(left, image=logo_image, text="").pack(side="left", padx=(0, 10))

text_frame = ctk.CTkFrame(left, fg_color="transparent")
text_frame.pack(side="left")

ctk.CTkLabel(
    text_frame,
    text="Pixel",
    font=FONTS["title"],
    text_color=COLORS["text"]
).pack(anchor="w")

ctk.CTkLabel(
    text_frame,
    text="AI Desktop Assistant",
    font=FONTS["subtitle"],
    text_color=COLORS["text_secondary"]
).pack(anchor="w")

# -------- STATUS --------
status_container = ctk.CTkFrame(header, fg_color="transparent")
status_container.pack(side="right", padx=16)

status_dot = ctk.CTkLabel(
    status_container,
    text="●",
    font=("Segoe UI", 16),
    text_color="#facc15"
)
status_dot.pack(side="left", padx=(0, 6))

status_text = ctk.CTkLabel(
    status_container,
    text="Idle",
    font=("Segoe UI", 12)
)
status_text.pack(side="left")

# ---------------- STATUS FUNCTION ----------------
def set_status(text, color=None):
    def update():
        status_text.configure(text=text)

        # Automatic theme colors
        if text == "Listening":
            dot_color = COLORS["success"]
            btn_color = COLORS["success"]

        elif text == "Recognizing":
            dot_color = COLORS["accent"]
            btn_color = COLORS["accent"]

        elif text == "Thinking":
            dot_color = COLORS["warning"]
            btn_color = COLORS["warning"]

        elif text == "Error":
            dot_color = COLORS["error"]
            btn_color = COLORS["error"]

        else:  # Idle
            dot_color = COLORS["warning"]
            btn_color = COLORS["surface2"]

        # If a custom color is supplied, use it (backward compatibility)
        if color is not None:
            dot_color = color

        status_dot.configure(text_color=dot_color)
        voice_btn.configure(fg_color=btn_color)

    app.after(0, update)

# ---------------- CHAT ----------------
chat_frame = ctk.CTkScrollableFrame(
    app,
    fg_color=COLORS["input"],
    corner_radius=18,
    border_width=0
)
chat_frame.pack(fill="both", expand=True, padx=12, pady=(10, 8))


def add_message(text, sender="pixel"):
    is_user = sender == "user"

    row = ctk.CTkFrame(chat_frame, fg_color="transparent")
    row.pack(fill="x", padx=10, pady=6)

    align = ctk.CTkFrame(row, fg_color="transparent")
    align.pack(anchor="e" if is_user else "w")

    MAX_PREVIEW = 180
    expanded = False

    def get_display_text():
        if expanded or len(text) <= MAX_PREVIEW:
            return text
        return text[:MAX_PREVIEW] + "..."

    bubble = ctk.CTkLabel(
        align,
        text=get_display_text(),
        wraplength=480,
        justify="left",
        corner_radius=20,
        font=FONTS["chat"],
        text_color=COLORS["text"],
        fg_color=(
        COLORS["user_bubble"]
        if is_user
        else COLORS["assistant_bubble"]
)
    )
    bubble.pack()

    def toggle():
        nonlocal expanded
        expanded = not expanded
        bubble.configure(text=get_display_text())
        toggle_btn.configure(text="Less" if expanded else "More")

    # 👉 Show button only if long message
    if len(text) > MAX_PREVIEW:
        toggle_btn = ctk.CTkButton(
            align,
            text="More",
            width=60,
            height=22,
            font=("Segoe UI", 10),
            fg_color="#374151",
            command=toggle
        )
        toggle_btn.pack(anchor="w", pady=(2, 0))

    time_label = ctk.CTkLabel(
        align,
        text=datetime.now().strftime("%H:%M"),
        font=("Segoe UI", 10),
        text_color="#6b7280"
    )
    time_label.pack(anchor="e" if is_user else "w")

    chat_frame.update_idletasks()
    chat_frame._parent_canvas.yview_moveto(1.0)
    
add_message("Hi. I am Pixel. How can I assist you?")

# ---------------- INPUT ----------------
input_frame = ctk.CTkFrame(app, fg_color="#0b0f14")
input_frame.pack(fill="x", padx=12, pady=(4, 6))

user_entry = ctk.CTkEntry(
    input_frame,
    placeholder_text="Type your message...",
    height=48,
    font=("Segoe UI", 14),
    fg_color=COLORS["surface"]
)
user_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))


def send_message():
    query = user_entry.get().strip()
    if not query:
        return

    add_message(query, "user")
    user_entry.delete(0, "end")

    set_status("Thinking", "#f59e0b")

    def process():
        response = handle_query(query)
        app.after(0, lambda: add_message(response, "pixel"))
        if not assistant_listening:
            set_status("Idle", "#facc15")

    threading.Thread(target=process, daemon=True).start()


user_entry.bind("<Return>", lambda e: send_message())

ctk.CTkButton(
    input_frame,
    text="Send",
    width=90,
    height=42,
    fg_color=COLORS["accent"],
    hover_color=COLORS["accent_hover"],
    text_color="#050816",
    corner_radius=16,
    font=FONTS["button"],
    command=send_message
).pack(side="right")

# ---------------- MIC ANIMATION ----------------
def animate_glow():
    global glow_job, glow_intensity, glow_direction

    if not assistant_listening:
        return

    glow_intensity += 10 * glow_direction

    if glow_intensity >= 255:
        glow_intensity = 255
        glow_direction = -1
    elif glow_intensity <= 80:
        glow_intensity = 80
        glow_direction = 1

    color = "#{:02x}{:02x}{:02x}".format(0, glow_intensity, 0)

    try:
        voice_btn.configure(border_color=color)
    except:
        pass

    glow_job = app.after(30, animate_glow)

# ---------------- VOICE ----------------
def toggle_voice():
    global assistant_listening

    if not assistant_listening:
        assistant_listening = True

        voice_btn.configure(
            text="Stop Listening",
            fg_color="#16a34a",
            border_width=3
        )

        set_status("Listening", "#22c55e")
        animate_glow()

        threading.Thread(
            target=run_assistant,
            args=(
                lambda msg: app.after(0, lambda: add_message(msg, "pixel")),
                lambda state, color: app.after(0, lambda: set_status(state, color))
            ),
            daemon=True
        ).start()

    else:
        assistant_listening = False
        stop_assistant()

        if glow_job:
            app.after_cancel(glow_job)

        voice_btn.configure(
            text="Start Listening",
            fg_color="#334155",
            border_width=1
        )

        set_status("Idle", "#facc15")
        add_message("Assistant stopped.")

# ---------------- CONTROLS ----------------
controls = ctk.CTkFrame(app, fg_color="transparent")
controls.pack(pady=10)

voice_btn = ctk.CTkButton(
    controls,
    text="Start Listening",
    width=240,
    height=56,
    corner_radius=18,
    font=FONTS["button"],
    fg_color=COLORS["surface2"],
    hover_color="#334155",
    command=toggle_voice
)
voice_btn.pack(side="left", padx=10)


def clear_chat():
    for w in chat_frame.winfo_children():
        w.destroy()
    add_message("Chat cleared.")


ctk.CTkButton(
    controls,
    text="Clear Chat",
    width=140,
    height=50,
    fg_color="#334155",
    command=clear_chat
).pack(side="left", padx=10)

app.mainloop()
