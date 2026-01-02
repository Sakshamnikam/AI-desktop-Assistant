import os
import pyautogui
from datetime import datetime
import webbrowser
import urllib.parse
import subprocess
import pyautogui
import time
import pywhatkit
import threading
from speechfunctions import speak


# ------------------ SYSTEM ACTIONS ------------------


def open_notepad():
    subprocess.Popen(["notepad.exe"])
    return "Opening Notepad."

def open_chrome():
    try:
        os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
    except:
        os.startfile("chrome")
    return "Opening Chrome."

def increase_volume():
    pyautogui.press("volumeup")
    return "Increasing volume."

def decrease_volume():
    pyautogui.press("volumedown")
    return "Decreasing volume."

def mute():
    pyautogui.press("volumemute")
    return "Muting audio."

def take_screenshot():
    folder = "Screenshots"
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
    path = os.path.join(folder, filename)

    pyautogui.screenshot(path)
    return f"Screenshot saved as {filename}."


def open_youtube():
    webbrowser.open("https://www.youtube.com")
    return "Opening YouTube."

def play_youtube_video(video_name):
    try:
        pywhatkit.playonyt(video_name)  # opens video
        time.sleep(2)                   # wait for YouTube tab to load
        pyautogui.press("space")        # auto-play the video
        return f"Playing {video_name} on YouTube."
    except Exception as e:
        return f"Could not play video: {e}"


def close_window():
    pyautogui.hotkey("alt", "f4")
    return "Closing the current window."

def open_cmd():
    try:
        subprocess.Popen("cmd.exe")
        return "Opening Command Prompt."
    except Exception as e:
        return f"Could not open Command Prompt: {e}"


def set_timer(query):
    try:
        words = query.lower().split()

        # Extract number from query (e.g., "10 minutes")
        duration = next((int(w) for w in words if w.isdigit()), None)

        if duration is None:
            return "Please tell me the duration for the timer."

        # Detect unit (seconds, minutes, hours)
        if "second" in query:
            seconds = duration
        elif "minute" in query:
            seconds = duration * 60
        elif "hour" in query:
            seconds = duration * 3600
        else:
            return "Please specify seconds, minutes, or hours."

        # Background thread for the timer
        def timer_thread():
            time.sleep(seconds)
            speak("Your timer is complete.")

        threading.Thread(target=timer_thread, daemon=True).start()

        return f"Timer for {duration} {('seconds' if seconds==duration else 'minutes' if seconds==duration*60 else 'hours')} started."

    except Exception as e:
        return f"I could not set the timer: {e}"


def create_file(query):
    q = query.lower()

    # 1️⃣ Extract filename
    # expected patterns: "file named X", "file called X", "create X"
    name = None
    if "named" in q:
        name = q.split("named")[-1].strip()
    elif "called" in q:
        name = q.split("called")[-1].strip()
    else:
        # fallback pattern
        words = q.split()
        if "create" in words:
            idx = words.index("create")
            if idx + 1 < len(words):
                name = words[idx + 1]

    if not name:
        return "Please tell me the file name."

    # Remove unwanted words
    name = name.replace("file", "").strip()
    
    # Add default extension if not provided
    if "." not in name:
        name += ".txt"

    # 2️⃣ Detect location
    # SPEECH → PATH mapping
    username = os.getlogin()
    locations = {
        "desktop": fr"C:\Users\{username}\Desktop",
        "documents": fr"C:\Users\{username}\Documents",
        "downloads": fr"C:\Users\{username}\Downloads",
        "c drive": r"C:",
        "d drive": r"D:",
    }

    folder_path = None
    for word, path in locations.items():
        if word in q:
            folder_path = path
            break

    # If no location specified → default to Desktop
    if folder_path is None:
        folder_path = fr"C:\Users\{username}\Desktop"

    # 3️⃣ Create the file
    file_path = os.path.join(folder_path, name)

    try:
        with open(file_path, "w") as f:
            f.write("")  # empty file
        return f"Created file {name} in {folder_path}."
    except Exception as e:
        return f"Could not create the file: {e}"

def google_search(query):
    text = query.lower().replace("google", "").replace("search", "").strip()
    if not text:
        return "What do you want me to search on Google?"
    webbrowser.open("https://www.google.com/search?q=" + urllib.parse.quote(text))
    return f"Searching Google for {text}"


def open_spotify():
    webbrowser.open("https://open.spotify.com")
    return "Opening Spotify in your browser"