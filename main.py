from speechfunctions import listen, speak, calibrate_mic,what_can_you_do
from actions import *
from aibrain import ask_ai

def handle_query(q):

    q = q.lower()

    if "what can you do" in q or "what all can you do" in q:
        return what_can_you_do()
    
    # --- SYSTEM COMMANDS ---

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
    
    if "close window" in q or "close this window" in q or "exit window" in q:
        return close_window()
    
    if "open command prompt" in q or "open cmd" in q:
        return open_cmd()

    if "set a timer" in q or "start a timer" in q or "timer" in q:
        return set_timer(q) 

    if "create file" in q or "make file" in q or "create a file" in q:
        return create_file(q)

    if "search google for" in q or q.startswith("google "):
        return google_search(q)

    
    # --- AI fallback ---
    return ask_ai(q)

def main():
    calibrate_mic()
    print("Pixel is ready...")

    # 🔊 Pixel speaks a greeting after startup
    speak("Hi, I am Pixel!")

    while True:
        query = listen()
        if not query:
            continue
        
        if "quit" in query or "bye" in query:
            speak("Goodbye!")
            break

        response = handle_query(query)

        print("Pixel:", response)
        speak(response)



if __name__ == "__main__":
    main()
