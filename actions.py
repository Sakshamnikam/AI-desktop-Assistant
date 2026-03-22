import os
import pyautogui
from datetime import datetime
import webbrowser
import urllib.parse
import subprocess
import time
import pywhatkit
import threading
import getpass
from speechfunctions import speak
import re
import cv2
import pygetwindow as gw

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

def increase_volume(query=None):
    steps = extract_volume_steps(query, default=5)

    for _ in range(steps):
        pyautogui.press("volumeup")

    return f"Increased volume by {steps} steps."


def decrease_volume(query=None):
    steps = extract_volume_steps(query, default=5)

    for _ in range(steps):
        pyautogui.press("volumedown")

    return f"Decreased volume by {steps} steps."


def extract_volume_steps(query, default=5):
    if not query:
        return default

    numbers = re.findall(r'\d+', query)

    if numbers:
        steps = int(numbers[0])

        # 🔒 Safety cap
        return min(max(steps, 1), 50)

    return default



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
    active = gw.getActiveWindow()
    
    if active and "Pixel" in active.title:
        return "I won’t close myself."
    
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

    # ---------------- 1. Detect location ----------------
    username = getpass.getuser()

    locations = {
        "desktop": f"C:\\Users\\{username}\\Desktop",
        "documents": f"C:\\Users\\{username}\\Documents",
        "downloads": f"C:\\Users\\{username}\\Downloads",
        "c drive": "C:\\",
        "d drive": "D:\\"
    }

    folder_path = None
    for key, path in locations.items():
        if key in q:
            folder_path = path
            q = q.replace(key, "")  # REMOVE location from sentence
            break

    # Default to Desktop
    if not folder_path:
        folder_path = f"C:\\Users\\{username}\\Desktop"

    # Prevent root C drive writing
    if folder_path in ["C:\\", "D:\\"]:
        return "For security reasons, files cannot be created directly in drive root."

    # ---------------- 2. Extract filename ----------------
    name = q.replace("create", "").replace("file", "").replace("named", "").replace("called", "")
    name = name.strip()

    # Remove invalid characters
    name = re.sub(r'[\\/:*?"<>|]', '', name)

    if not name:
        return "Please specify a valid file name."

    if "." not in name:
        name += ".txt"

    # ---------------- 3. Create file ----------------
    file_path = os.path.join(folder_path, name)

    try:
        with open(file_path, "w") as f:
            f.write("")
        return f"File '{name}' created successfully in {folder_path}."

    except Exception as e:
        return f"Failed to create file: {e}"

def google_search(query):
    text = query.lower().replace("google", "").replace("search", "").strip()
    if not text:
        return "What do you want me to search on Google?"
    webbrowser.open("https://www.google.com/search?q=" + urllib.parse.quote(text))
    return f"Searching Google  {text}"


def open_spotify():
    webbrowser.open("https://open.spotify.com")
    return "Opening Spotify in your browser"

def open_linkedin():
    webbrowser.open("https://www.linkedin.com/")
    return "Opening LinkedIn in your browser"


def open_folder(query):
    import os
    import subprocess
    import getpass
    import re

    q = query.lower()
    username = getpass.getuser()

    # ---------------- DIRECT FOLDER MAPPING ----------------
    system_folders = {
        "desktop": f"C:\\Users\\{username}\\Desktop",
        "downloads": f"C:\\Users\\{username}\\Downloads",
        "documents": f"C:\\Users\\{username}\\Documents",
        "pictures": f"C:\\Users\\{username}\\Pictures",
        "music": f"C:\\Users\\{username}\\Music",
        "videos": f"C:\\Users\\{username}\\Videos",
    }

    for name, path in system_folders.items():
        if name in q:
            if os.path.exists(path):
                subprocess.Popen(f'explorer "{path}"')
                return f"Opening {name.capitalize()} folder."
            else:
                return f"{name.capitalize()} folder not found."

    # ---------------- DRIVE HANDLING ----------------
    drive_match = re.search(r"\b([a-z])\s*(drive)?\b", q)
    if drive_match:
        drive = drive_match.group(1).upper() + ":\\" 
        if os.path.exists(drive):
            subprocess.Popen(f'explorer "{drive}"')
            return f"Opening {drive} drive."
        else:
            return f"{drive} drive not found."

    # ---------------- SEARCH FALLBACK ----------------
    clean_q = (
        q.replace("open", "")
         .replace("folder", "")
         .replace("the", "")
         .strip()
    )

    search_paths = [
        f"C:\\Users\\{username}\\Desktop",
        f"C:\\Users\\{username}\\Documents",
        f"C:\\Users\\{username}\\Downloads",
    ]

    matches = []

    for base in search_paths:
        for root, dirs, _ in os.walk(base):
            for d in dirs:
                if clean_q in d.lower():
                    matches.append(os.path.join(root, d))
            if len(matches) >= 3:
                break

    if matches:
        subprocess.Popen(f'explorer "{matches[0]}"')
        return f"Opening {os.path.basename(matches[0])} folder."

    return f"I couldn't find any folder named {clean_q}."



def _camera_loop():
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        return

    cv2.namedWindow("Pixel Camera")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        cv2.imshow("Pixel Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


def open_camera():
    threading.Thread(target=_camera_loop, daemon=True).start()
    return "Turning on camera."

def take_picture():
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        return "Camera not detected."

    ret, frame = cam.read()
    cam.release()

    if not ret:
        return "Failed to capture image."

    # Create Pictures folder if not exists
    folder = "Pictures"
    os.makedirs(folder, exist_ok=True)

    filename = datetime.now().strftime("photo_%Y%m%d_%H%M%S.jpg")
    path = os.path.join(folder, filename)

    cv2.imwrite(path, frame)

    return "Picture captured and saved successfully."