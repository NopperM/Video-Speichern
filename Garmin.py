import speech_recognition as sr
import pyautogui
import pygame
from time import sleep
from threading import Thread


pygame.mixer.init()

recognizer = sr.Recognizer()
activation_phrases = [ #Ignore why so many dumbass words the fucking speech recognizer thing is stupid
    "okay garmin",
    "ok garmin",
    "okay garn",
    "ok garn", 
    "okay car",
    "ok car",
    "okay carmen",
    "ok carmen",
    "okay garland",
    "ok google",
    "okay gar",
    "ok google"
]
command_phrase = "video speichern"

def play_sound(file_path):
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error playing sound: {e}")

def delayed_hotkey():
    sleep(2)
    pyautogui.hotkey('alt', 'f10')

def listen_for_commands():
    with sr.Microphone() as source:
        print("Listening for activation...")
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
        except sr.WaitTimeoutError:
            return
        
    try:
        text = recognizer.recognize_google(audio, language="de-DE").lower()
        print(f"Heard: {text}")
        
        
        if any(phrase in text for phrase in activation_phrases):
            print(f"Activation detected! (Heard: {text})")
            play_sound("activate.mp3")
            
            print("Listening for command...")
            with sr.Microphone() as source:
                try:
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
                    command_text = recognizer.recognize_google(audio, language="de-DE").lower()
                    print(f"Command: {command_text}")
                    
                    if command_phrase in command_text:
                        play_sound("confirm.mp3")
                        Thread(target=delayed_hotkey).start()
                except sr.WaitTimeoutError:
                    print("No command detected")
                    
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"API error: {e}")

if __name__ == "__main__":
    while True:
        listen_for_commands()
        sleep(0.5)