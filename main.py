from speechfunctions import listen, speak, calibrate_mic, what_can_you_do
from actions import *
from aibrain import ask_ai

# 🔹 REQUIRED FOR GUI CONTROL
assistant_running = False

def handle_query(q):
    q = q.lower()

    if "what can you do" in q or "what all can you do" in q:
        return what_can_you_do()

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
    if "create file" in q:
        return create_file(q)
    if "google" in q:
        return google_search(q)

    return ask_ai(q)

# 🔹 GUI WILL CALL THIS
def run_assistant(log_callback=None):
    global assistant_running
    assistant_running = True

    calibrate_mic()

    if log_callback:
        log_callback("Pixel: Hi, I am Pixel!")
    speak("Hi, I am Pixel!")

    while assistant_running:
        query = listen()
        if not query:
            continue

        if log_callback:
            log_callback(f"You: {query}")

        if "quit" in query or "bye" in query:
            if log_callback:
                log_callback("Pixel: Goodbye!")
            speak("Goodbye!")
            assistant_running = False
            break

        response = handle_query(query)

        if log_callback:
            log_callback(f"Pixel: {response}")

        speak(response)


# 🔹 GUI STOP BUTTON
def stop_assistant():
    global assistant_running
    assistant_running = False
