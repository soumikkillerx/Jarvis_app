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






"""Code Analysis


Code Analysis


1. Initialization

nlp: Loads the English language model from SpaCy for Natural Language Processing (NLP).
recognizer: Initializes the speech recognizer.
tts_engine: Initializes the text-to-speech engine.

2. Greetings

A list of greetings is randomly selected and spoken when the application starts.
3. Command Handling

start_recognition: Continuously listens for voice input and processes the commands using the recognize_speech and handle_command methods.
4. Voice Command Processing

recognize_speech: Converts audio input to text using Google's speech recognition service.

speak_text: Converts text to speech and speaks it out loud.

handle_command: Processes the recognized text and performs actions based on specific commands.






Voice Commands and Corresponding Actions


1. Search Command

Trigger: "search <query>"
Example: If you say "search Python programming", the application will open Google and search for "Python programming".
Code Handling: The text is parsed to extract the query, which is then used to construct a Google search URL.


2. YouTube Command

Trigger: "open YouTube" or "open youtube"
Example: If you say "open YouTube", the application will open YouTube in the default web browser.
Code Handling: Opens the YouTube website.


3. Time Command

Trigger: "time"
Example: If you say "what time is it", the application will respond with the current time.
Code Handling: Retrieves the current time using the datetime module and speaks it out.



4. Joke Command

Trigger: "tell me a joke"
Example: If you say "tell me a joke", the application will respond with a random joke.
Code Handling: Fetches a random joke using the pyjokes library and speaks it out.



5. Reminder Command

Trigger: "set reminder"
Example: If you say "set a reminder", the application sets a reminder for 10 seconds (hardcoded) and then speaks the reminder message.
Code Handling: Uses threading to wait for the specified time and then speaks the reminder message.




6. Exit Command

Trigger: "exit" or "quit"
Example: If you say "exit" or "quit", the application will terminate.
Code Handling: Exits the application by calling exit().



7. Default Response

Trigger: Any command that does not match the predefined commands.
Example: If you say "play music", which is not a defined command, the application will respond with "I don't know how to respond to that."
Code Handling: Provides a default response for unrecognized commands."""
