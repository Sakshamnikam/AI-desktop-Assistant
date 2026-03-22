
from speechfunctions import listen, speak, calibrate_mic, what_can_you_do
from actions import *
from aibrain import ask_ai
import threading

# ---------------- GLOBAL STATE ----------------
assistant_running = False
WAKE_WORD = "hey pixel"


# ---------------- QUERY HANDLER ----------------
def handle_query(q):
        
        q = q.lower().strip()

        # -------- NORMALIZE --------
        q = q.replace("please", "").replace("could you", "").replace("can you", "").strip()

        # -------- HELP --------
        if any(p in q for p in ["what can you do", "your features", "help"]):
            return what_can_you_do()

        # -------- APP LAUNCH --------
        if any(p in q for p in ["open notepad", "start notepad", "launch notepad"]):
            return open_notepad()

        if any(p in q for p in ["open chrome", "start chrome", "launch chrome", "open browser"]):
            return open_chrome()

        if any(p in q for p in ["open cmd", "command prompt", "terminal"]):
            return open_cmd()

        # -------- VOLUME --------
        if any(p in q for p in ["increase volume", "volume up", "raise volume"]):
            return increase_volume()

        if any(p in q for p in ["decrease volume", "volume down", "lower volume"]):
            return decrease_volume()

        if any(p in q for p in ["mute", "silence"]):
            return mute()

        # -------- SCREEN --------
        if any(p in q for p in ["screenshot", "take screenshot", "capture screen"]):
            return take_screenshot()

        # -------- YOUTUBE --------
        if any(p in q for p in ["open youtube", "go to youtube"]):
            return open_youtube()

        if "youtube" in q and any(p in q for p in ["play", "search", "watch"]):
            video = (
                q.replace("play", "")
                .replace("search", "")
                .replace("watch", "")
                .replace("on youtube", "")
                .replace("youtube", "")
                .strip()
            )
            return play_youtube_video(video)

        # -------- WINDOW CONTROL --------
        if any(p in q for p in ["close window", "close this", "close current window"]):
            return close_window()

        # -------- TIMER --------
        if any(p in q for p in ["timer", "set timer", "countdown"]):
            return set_timer(q)

        # -------- FILE --------
        if any(p in q for p in ["create file", "make file", "new file", "create a file"]):
            return create_file(q)

        # -------- SEARCH --------
        if q.startswith(("google ", "search ")) or "search for" in q:
            return google_search(q)

        # -------- WEB APPS --------
        if any(p in q for p in ["open spotify", "start spotify"]):
            return open_spotify()

        if any(p in q for p in ["open linkedin", "linkedin"]):
            return open_linkedin()

        # -------- FILE SYSTEM --------
        if "open" in q and any(p in q for p in ["folder", "drive", "directory"]):
            return open_folder(q)

        # -------- CAMERA --------
        if any(p in q for p in ["take picture", "click photo", "capture photo"]):
            return take_picture()

        if any(p in q for p in ["open camera", "start camera", "turn on camera"]):
            return open_camera()

        # -------- FALLBACK AI --------
        return ask_ai(q)




# ---------------- MAIN ASSISTANT LOOP ----------------
def run_assistant(log_callback=None, status_callback=None):
    global assistant_running

    # Prevent multiple threads
    if assistant_running:
        return

    assistant_running = True
    calibrate_mic()

    awake = False

    if log_callback:
        log_callback("Pixel is ready. Say 'Hey Pixel'.")

    while assistant_running:

        # 🟢 Listening
        if status_callback:
            status_callback("Listening", "#22c55e")

        query = listen()

        # 🔴 HARD STOP CHECK
        if not assistant_running:
            break

        # Ignore noise / silence
        if not query or query == "__unrecognized__":
            continue

        # 🔵 Recognizing
        if status_callback:
            status_callback("Recognizing", "#3b82f6")

        query = query.lower().strip()

        # 💤 Wake word system
        if not awake:
            if WAKE_WORD in query:
                awake = True
                speak("Yes, I am listening.")
                if log_callback:
                    log_callback("🟢 Wake word detected")
            continue

        # 🛑 Sleep commands
        if any(word in query for word in ["bye", "stop", "sleep", "exit"]):
            speak("Going to sleep.")
            awake = False
            if log_callback:
                log_callback("🔴 Assistant sleeping")
            continue

        if log_callback:
            log_callback(f"You: {query}")

        # 🟡 Thinking
        if status_callback:
            status_callback("Thinking", "#facc15")

        response = handle_query(query)

        if response:
            if log_callback:
                log_callback(f"Pixel: {response}")

            # 🔊 Speak in background
            threading.Thread(
                target=speak,
                args=(response,),
                daemon=True
            ).start()

    # 🔴 Clean exit
    assistant_running = False

    if status_callback:
        status_callback("Idle", "#facc15")


# ---------------- STOP FUNCTION ----------------
def stop_assistant():
    global assistant_running
    assistant_running = False
