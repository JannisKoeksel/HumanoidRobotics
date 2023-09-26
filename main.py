from states import StateMashie
import pyttsx3
import face_recognition

engine = pyttsx3.init()
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('rate', 100) 
engine.setProperty('voice', voices[1].id)
print('setup complete')

engine.say('test')
engine.runAndWait()