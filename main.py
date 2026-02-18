from speechfunctions import listen, speak, calibrate_mic, what_can_you_do
from actions import *
from aibrain import ask_ai
import threading

# 🔹 REQUIRED FOR GUI CONTROL
assistant_running = False
WAKE_WORD = "hey pixel"


def handle_query(q):
    q = q.lower().strip()

    # ----- CAPABILITIES -----
    if "what can you do" in q or "what all can you do" in q :
        return what_can_you_do()

    # ----- SYSTEM COMMANDS -----
    if "open notepad" in q:
        return open_notepad()

    if "open chrome" in q:
        return open_chrome()

    if "increase volume" in q:
        return increase_volume()

    if "decrease volume" in q:
        return decrease_volume()

    if "mute" in q:
        return mute()

    if "screenshot" in q:
        return take_screenshot()

    if "open youtube" in q:
        return open_youtube()

    if "play" in q and "youtube" in q:
        video = q.replace("play", "").replace("on youtube", "").strip()
        return play_youtube_video(video)

    if "close window" in q:
        return close_window()

    if "open command prompt" in q or "open cmd" in q:
        return open_cmd()

    if "timer" in q:
        return set_timer(q)

    create_keywords = [
    "create file",
    "make file",
    "new file",
    "create a file"
]
    if any(kw in q for kw in create_keywords):
        return create_file(q)


    # 🔴 FIXED: Google search ONLY when user explicitly asks to search
    if q.startswith(("google ", "search ")):
        return google_search(q)

    if "open spotify" in q or "start spotify" in q:
        return open_spotify()

    if "open linkedin" in q:
        return open_linkedin()
    
    if "open" in q and ("folder" in q or "drive" in q):
        return open_folder(q)
    
    if "take a picture" in q or "take picture" in q or "take a photo" in q or "click photo" in q:
        return take_picture()

    if "open camera" in q or "turn on camera" in q or "start camera" in q:
        return open_camera()
    

    return ask_ai(q)


# 🔹 GUI WILL CALL THIS
def run_assistant(log_callback=None, status_callback=None):
    global assistant_running
    assistant_running = True

    calibrate_mic()
    awake = False

    if log_callback:
        log_callback("Pixel is ready. Say 'Hey Pixel' to activate.")

    while assistant_running:

        if status_callback:
            status_callback("Listening", "#22c55e")

        query = listen()

        if not query or query == "__unrecognized__":
            continue

        if status_callback:
            status_callback("Recognizing", "#3b82f6")

        query = query.lower()

        # 💤 Sleep Mode
        if not awake:
            if "hey pixel" in query:
                awake = True
                speak("Yes, I am listening.")
                if log_callback:
                    log_callback("🟢 Wake word detected")
            continue

        # 🛑 Exit
        if any(word in query for word in ["bye", "stop", "sleep", "exit"]):
            speak("Okay, going to sleep.")
            awake = False
            if log_callback:
                log_callback("🔴 Assistant sleeping")
            continue

        if log_callback:
            log_callback(f"You: {query}")

        if status_callback:
            status_callback("Thinking", "#facc15")

        response = handle_query(query)

        if response:
            if log_callback:
                log_callback(f"Pixel: {response}")

            # Speak in background thread
            threading.Thread(
                target=speak,
                args=(response,),
                daemon=True
            ).start()


        if status_callback:
            status_callback("Listening", "#22c55e")





# 🔹 GUI STOP BUTTON
def stop_assistant():
    global assistant_running
    assistant_running = False
