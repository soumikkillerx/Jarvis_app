import speech_recognition as sr
import pyttsx3
import spacy
import webbrowser
from datetime import datetime
import time
import threading
import pyjokes
import random

# Initialize NLP model
nlp = spacy.load("en_core_web_sm")

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# List of greetings
greetings = [
    "Hello! How can I assist you today?",
    "Hi there! What can I do for you?",
    "Greetings! How may I help you?",
    "Hey! What would you like to do today?",
    "Hi! How can I make your day better?"
]

class JARVIS:
    def __init__(self):
        self.speak_text(random.choice(greetings))
        self.start_recognition()

    def start_recognition(self):
        while True:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source)
                text = self.recognize_speech(audio)
                print(f"You said: {text}")
                self.handle_command(text)

    def recognize_speech(self, audio):
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Sorry, the service is down."

    def speak_text(self, text):
        print(f"JARVIS says: {text}")
        tts_engine.say(text)
        tts_engine.runAndWait()

    def handle_command(self, text):
        doc = nlp(text)

        if "search" in text:
            query = text.replace("search", "").strip()
            if query:
                webbrowser.open(f"https://www.google.com/search?q={query}")
                self.speak_text(f"Searching for {query}.")
            else:
                self.speak_text("What do you want to search for?")
        elif "open" in text and "youtube" in text:
            webbrowser.open("http://www.youtube.com")
            self.speak_text("Opening YouTube.")
        elif "time" in text:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            self.speak_text(f"The current time is {current_time}.")
        elif "tell me a joke" in text:
            joke = pyjokes.get_joke()
            self.speak_text(joke)
        elif "set reminder" in text:
            reminder_time = 10  # Set reminder time in seconds
            reminder_message = "This is your reminder!"  # Set your reminder message
            self.speak_text(f"Setting a reminder for {reminder_time} seconds.")
            self.set_reminder(reminder_time, reminder_message)
        elif "exit" in text or "quit" in text:
            self.speak_text("Goodbye! See you soon.")
            exit()  # Exit the program
        else:
            self.speak_text("I don't know how to respond to that.")

    def set_reminder(self, reminder_time, message):
        def reminder():
            time.sleep(reminder_time)
            self.speak_text(message)
        thread = threading.Thread(target=reminder)
        thread.start()

if __name__ == "__main__":
    JARVIS()
