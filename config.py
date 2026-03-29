import os
from dotenv import load_dotenv
import speech_recognition as sr

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Shared recognizer (calibrated once)
recognizer = sr.Recognizer()

# Conversation memory list
conversation_history = []
