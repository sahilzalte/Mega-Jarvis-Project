# Quick Mic Test Script
import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Speak something...")
    audio = r.listen(source)
try:
    print("You said:", r.recognize_google(audio))
except Exception as e:
    print("Error:", e)