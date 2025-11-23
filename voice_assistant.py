import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
user_name = None 

# ---------- TEXT TO SPEECH SETUP ----------
engine = pyttsx3.init()

def speak(text: str):
    """Convert text to speech."""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


# ---------- SPEECH TO TEXT ----------
def listen() -> str | None:
    """Listen from the microphone and return recognized text."""
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\n[Listening...]")
        r.pause_threshold = 0.8
        audio = r.listen(source)

    try:
        print("[Recognizing...]")
        query = r.recognize_google(audio, language="en-IN")  # or "en-US"
        print(f"You said: {query}")
        return query
    except sr.UnknownValueError:
        speak("Sorry, I could not understand. Please repeat.")
    except sr.RequestError:
        speak("Sorry, I'm having trouble reaching the speech service.")
    
    return None


# ---------- NLP / COMMAND HANDLER ----------

def handle_command(command: str) -> bool:
    """
    Process the user's command.
    Return False if the assistant should stop, True to continue.
    """
    global user_name
    cmd = command.lower()

    # --- LEARN YOUR NAME ---
    if "my name is" in cmd:
        name_part = cmd.split("my name is", 1)[1].strip()
        if name_part:
            # Capitalize nicely: "dikshita" -> "Dikshita"
            user_name = " ".join(w.capitalize() for w in name_part.split())
            speak(f"Nice to meet you, {user_name}. I will remember your name.")
        else:
            speak("I did not catch your name. Please say: my name is, and then your name.")
        return True

    # --- TELL YOU YOUR NAME ---
    if "what is my name" in cmd or "do you know my name" in cmd:
        if user_name:
            speak(f"Your name is {user_name}.")
        else:
            speak("I don't know your name yet. Please tell me by saying: my name is, and then your name.")
        return True

    # --- REACT WHEN IT HEARS YOUR NAME ---
    if user_name and user_name.lower() in cmd:
        speak(f"Yes {user_name}, I'm listening.")
        # we still continue to handle the rest of the command below

    # Exit commands
    if any(word in cmd for word in ["exit", "quit", "stop", "bye"]):
        speak("Goodbye! It was nice talking to you.")
        return False

    # Time
    if "time" in cmd:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}.")
        return True

    # Date
    if "date" in cmd or "day" in cmd:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today is {today}.")
        return True

    # Your name (assistant's own name)
    if "your name" in cmd or "who are you" in cmd:
        speak("I am your Python voice assistant.")
        return True

    # Open YouTube
    if "open youtube" in cmd:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
        return True

    # Open Google
    if "open google" in cmd:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")
        return True

    # Simple search on Google
    if "search for" in cmd:
        query = cmd.split("search for", 1)[1].strip()
        if query:
            speak(f"Searching for {query}.")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            speak("What should I search for?")
        return True

    # Joke
    if "joke" in cmd:
        speak("Why do programmers prefer dark mode? Because light attracts bugs.")
        return True

    # Fallback: repeat what user said
    speak("You said: " + command)
    return True


# ---------- MAIN LOOP ----------
def main():
    speak("Hello, I am your AI voice assistant. How can I help you?")

    while True:
        command = listen()
        if not command:
            continue  # try listening again
        
        should_continue = handle_command(command)
        if not should_continue:
            break


if __name__ == "__main__":
    main()
