import speech_recognition as sr
import time

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)
    
print("speach done")
print("time", time.time())
try:
    print("Whisper thinks you said " + r.recognize_whisper(audio, language="english", model ="tiny.en"))
except sr.UnknownValueError:
    print("Whisper could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Whisper")
print("time", time.time())