# 🤖 Pixel – AI Desktop Assistant

Pixel is a **voice-controlled AI desktop assistant for Windows** that can perform system actions, respond intelligently using **Groq LLM**, and interact through **speech recognition and text-to-speech**.

---

## ✨ Features

### 🎙️ Voice Interaction

* Listens to your voice commands
* Responds using natural-sounding speech (TTS)

### 🖥️ System Control

You can say commands like:

* Open Notepad / Chrome
* Increase, decrease, or mute volume
* Take screenshots
* Open Command Prompt
* Close current window

### ⏱️ Utility Commands

* Set timers (seconds, minutes, hours)
* Create files on Desktop / Documents / Downloads
* Google search using voice

### ▶️ YouTube Control

* Open YouTube
* Play any video directly by voice

### 🧠 AI Chat (Fallback)

* Uses **Groq API (LLaMA 3.3 70B)**
* Maintains short conversation memory
* Friendly assistant personality named **Pixel**

---

## 🗂️ Project Structure

```
AI_desktop_Assistant/
│
├── main.py              # Entry point
├── actions.py           # System & utility actions
├── aibrain.py           # AI logic using Groq API
├── speechfunctions.py   # Speech recognition & TTS
├── config.py            # Environment & shared config
├── .env                 # API keys (NOT committed)
├── .gitignore
└── README.md
```

---

## ⚙️ Requirements

* Python 3.9+
* Windows OS
* Microphone

### 📦 Python Libraries

Install all dependencies using:

```bash
pip install speechrecognition pyttsx3 pyautogui python-dotenv groq pywhatkit pytube
```

---

## 🔐 Environment Setup

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_groq_api_key_here
```

⚠️ **Never commit `.env` to GitHub**

---

## ▶️ How to Run

```bash
python main.py
```

Pixel will:

1. Calibrate your microphone
2. Greet you
3. Start listening for commands

Say **"bye"** or **"quit"** to exit.

---

## 🗣️ Commands Pixel can Perform

* "Open Chrome"
* "Search Google for"
* "Open Command Prompt"
* "Increase/Decrease/Mute volume "
* "Take a screenshot"
* "Set a timer for 10 minutes"
* "Create file named (file name) on desktop"
* "Play (Vidoe name) on YouTube"
* "Close Current Window"
* "Open Notepad"

* Pixel can answer any General Knowledge questions for ex- What is artificial intelligence?"

---

## 🧠 AI Model

* **Provider:** Groq
* **Model:** LLaMA 3.3 70B Versatile
* Optimized for **short, friendly responses**

---

## 🚀 Future Improvements

* Wake word support ("Hey Pixel")
* Linux & macOS support
* GUI interface
* App control (Spotify, VS Code)
* Persistent conversation memory

---

## 👨‍💻 Author

**Saksham Nikam**

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!
