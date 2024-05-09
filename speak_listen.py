import pyttsx3
import speech_recognition as sr
from time import sleep
from pathlib import Path
import re
import datetime

#  se puede preguntar al usuario donde quiere guardar el archivo
#  libreria logging - para hacer el print

#  libreria get text (idioma)


class Recognizer:

    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 130)
        self.engine.setProperty("voice", "english")
        self.recognizer = sr.Recognizer()

    def speak(self, text: str):
        """Return text in audio voice"""
        self.engine.say(text)
        self.engine.runAndWait()
        return self.engine

    def hear_me(self):
        """Recognize user voice in text"""
        with sr.Microphone() as source:
            print("Listening...")
            audio = self.recognizer.listen(source)

            try:
                text = self.recognizer.recognize_google(audio, language="ES")
                print(f"I understood: {text}")
                sleep(2)
                return text, audio
            except sr.UnknownValueError:
                return None, None

    def save(self):
        """Ask to user about how to save data (text, audio, exit)"""
        Recognizer.speak(self, "Next, say text for save in text file. "
                         "Say audio for save in audio file. "
                         "Say exit for leave program")
        user_input, _ = Recognizer.hear_me(self)
        return user_input


def user_desktop_path():
    """Take the user path"""
    desktop_path = f"{Path.home()}/Desktop/"
    return desktop_path


def identify_input(user_input, patterns=["^([A-Za-z]+)$"]):
    """Identify the user answer about how to save data (text, audio, exit)"""
    new_user_input = None
    for pattern in patterns:
        try:
            new_user_input = re.findall(pattern, user_input)[0]
        except IndexError:
            pass
    return new_user_input


def save_file_choice(recognizer, text, audio, new_user_input, desktop_path):
    """User choice about saving data"""
    date = str(datetime.datetime.now())  # pasar de date.time a str
    print(date)

    if new_user_input == "exit":
        recognizer.speak("Leaving the program")
        return

    if new_user_input == "text":
        recognizer.speak("Understood, saving text")
        txt = f"Voice note.txt"
        with open(desktop_path + txt, "w") as text_file:
            text_file.write(f"Voice note date {date}:\n {text}")
        return text_file

    if new_user_input == "audio":
        recognizer.speak("Understood, saving audio")
        voice_note = "Voice-note-.wav"
        with open(desktop_path + voice_note, "wb") as audio_file:
            audio_file.write(audio.get_wav_data())
        return audio_file


def main():
    """Starting the program. The bot speak"""
    recognizer = Recognizer()
    # The bot speak
    recognizer.speak("We will proceed to save your voice note, listening...")
    desktop_path = user_desktop_path()  # Identify the user path
    # Recognize user voice, and take 2 values (text, audio)
    text, audio = recognizer.hear_me()
    # Ask to user about how to save data and take the value (user_input)
    user_input = recognizer.save()
    new_user_input = identify_input(user_input)  # Identify user input
    save_file_choice(recognizer, text, audio, new_user_input,
                     desktop_path)  # Save file user choice


if __name__ == "__main__":
    main()
