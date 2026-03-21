# 🤖 Pixel – AI Desktop Assistant

> A powerful **voice-controlled AI desktop assistant for Windows** that executes system commands, interacts conversationally using LLMs, and provides a seamless human-computer interaction experience.

---

## 🚀 Overview

**Pixel** is a smart desktop assistant inspired by systems like JARVIS. It combines:

* 🎙️ Voice recognition
* 🔊 Natural text-to-speech
* 🧠 AI-powered conversation (Groq LLaMA 3.3 70B)
* 🖥️ Direct system control

All wrapped inside a modern **CustomTkinter GUI**.

---

## ✨ Key Features

### 🎙️ Voice Interaction

* Real-time voice command recognition
* Wake word detection: **"Hey Pixel"**
* Natural AI-generated speech responses

### 🖥️ System Automation

Control your system hands-free:

* Open apps (Chrome, Notepad, CMD)
* Control volume (increase, decrease, mute)
* Take screenshots
* Close active window
* Browse folders and drives
* Open camera & capture images

### ⚙️ Productivity Utilities

* ⏱️ Smart timers (seconds, minutes, hours)
* 📁 File creation (Desktop/Documents/Downloads)
* 🌐 Google search via voice

### ▶️ Media Control

* Open YouTube
* Play videos using voice commands

### 🧠 AI Assistant (Fallback Engine)

* Powered by **Groq LLaMA 3.3 70B**
* Maintains short-term conversation memory
* Handles:

  * General queries
  * Coding help
  * Error solving

---

## 🧱 Architecture Overview

```
User Voice / Input
        ↓
Speech Recognition (speechfunctions.py)
        ↓
Command Handler (main.py)
        ↓
 ┌───────────────┬────────────────┐
 │               │                │
Actions Engine   AI Brain         Utilities
(actions.py)     (aibrain.py)     (config.py)
 │               │
System Control   Groq API (LLM)
```

---

## 📂 Project Structure

```
AI_desktop_Assistant/
│
├── gui.py               # Modern UI (CustomTkinter)
├── main.py              # Core assistant loop & command routing
├── actions.py           # System-level operations
├── aibrain.py           # LLM integration (Groq API)
├── speechfunctions.py   # Speech recognition & TTS
├── config.py            # Environment & shared state
├── .env                 # API keys (ignored)
├── README.md
```

---

## ⚙️ Tech Stack

* **Language:** Python
* **GUI:** CustomTkinter
* **Speech Recognition:** SpeechRecognition (Google API)
* **Text-to-Speech:** Edge-TTS + Pygame
* **Automation:** PyAutoGUI
* **AI Engine:** Groq (LLaMA 3.3 70B)
* **Media & Tools:** OpenCV, PyWhatKit

---

## 📦 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/pixel-ai-assistant.git
cd pixel-ai-assistant
```

### 2️⃣ Install Dependencies

```bash
pip install speechrecognition pyttsx3 pyautogui python-dotenv groq pywhatkit pytube customtkinter opencv-python pygame edge-tts
```

---

## 🔐 Environment Setup

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

⚠️ Never push `.env` to GitHub.

---

## ▶️ Running the Assistant

```bash
python gui.py
```

### 🔄 Workflow

1. App launches GUI
2. Microphone calibrates
3. Say **"Hey Pixel"**
4. Give commands

Say:

* **"sleep"** → pause
* **"bye" / "exit"** → stop

---

## 🗣️ Example Commands

```
"Hey Pixel, open Chrome"
"Set a timer for 10 minutes"
"Play lo-fi music on YouTube"
"Create file named notes on desktop"
"Take a screenshot"
"Search Google for AI tools"
"Open D drive"
"Click photo"
```

---

## 🧠 AI Configuration

* **Provider:** Groq
* **Model:** LLaMA 3.3 70B Versatile
* **Response Style:**

  * Short, precise
  * Structured
  * Minimal verbosity

---

## 🖼️ UI Highlights

* Dark modern interface
* Chat-style conversation window
* Voice toggle with animated glow
* Expandable code blocks
* Real-time status indicator

---

## 🚀 Future Enhancements

* 🌍 Multi-language voice support
* 🐧 Linux & macOS compatibility
* 💾 Persistent memory (long-term context)
* 🧠 Smarter command classification (NLP intent detection)
* 🔄 Auto-updater
* 🎯 App-specific automation (VS Code, Spotify native control)

---

## 👨‍💻 Author

**Saksham Nikam**

---

## ⭐ Show Your Support

If you found this project useful:

* ⭐ Star the repository
* 🍴 Fork it
* 🧠 Contribute new features

---

## ⚠️ Disclaimer

This assistant performs system-level actions. Use responsibly and review permissions before running on critical systems.

---
