import speech_recognition as sr
import pyttsx3
import time

# No global engine — we create a fresh one every time
# Windows engine gets stuck after first run if reused


# ---------------- SPEAK ---------------- #
def speak(text):
    text = str(text).strip()
    if not text:
        return

    print("Pixel:", text)

    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 175)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"[TTS ERROR] {e}")


# ---------------- LISTEN ---------------- #
def listen() -> str:
    r = sr.Recognizer()
    r.energy_threshold = 400
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.8
    r.non_speaking_duration = 0.5

    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = r.listen(source, timeout=None, phrase_time_limit=10)
        except:
            return ""

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-IN")
        print(f"You said: {query}")
        return query

    except sr.UnknownValueError:
        return ""   # ⬅️ ignore background noise silently

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
