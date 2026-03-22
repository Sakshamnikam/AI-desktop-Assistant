import speech_recognition as sr
import pyttsx3
import asyncio
import edge_tts
import pygame
import threading
import uuid
import os


engine = pyttsx3.init()
engine.setProperty("rate", 185)


# ---------------- SPEAK ---------------- #
pygame.mixer.init()

def speak(text):
    text = str(text).strip()
    if not text:
        return

    def _worker():
        try:
            # Unique filename every time
            file_name = f"tts_{uuid.uuid4().hex}.mp3"

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            communicate = edge_tts.Communicate(
                text,
                voice="en-GB-RyanNeural"
            )

            loop.run_until_complete(
                communicate.save(file_name)
            )
            loop.close()

            # Stop previous playback
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()

            pygame.mixer.music.load(file_name)
            pygame.mixer.music.play()

            # Cleanup after playback
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            pygame.mixer.music.unload()
            os.remove(file_name)

        except Exception as e:
            print("TTS ERROR:", e)

    threading.Thread(target=_worker, daemon=True).start()

# ---------------- LISTEN ---------------- #
def listen() -> str:
    r = sr.Recognizer()
    r.energy_threshold = 400
    r.dynamic_energy_threshold = True
    r.pause_threshold = 1.5
    r.non_speaking_duration = 0.7

    with sr.Microphone() as source:
        print("Listening...")

        try:
            audio = r.listen(source, timeout=3, phrase_time_limit=8)
        except:
            return ""

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-IN")
        print(f"You said: {query}")
        return query

    except sr.UnknownValueError:
        return "__unrecognized__"   # ⬅️ ignore background noise silently

    except sr.RequestError:
        print("Internet error — speech recognition unavailable.")
        return ""

# ---------------- CALIBRATE MIC ---------------- #
def calibrate_mic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Calibrating microphone…")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Mic ready.")

def what_can_you_do():
    return (
        "I can open apps,close current open window, control volume, take screenshots, "
        "play YouTube videos, set timers, create files, "
        "search Google, Click photos  and answer general questions. and many more what do you want me to do?"
    )