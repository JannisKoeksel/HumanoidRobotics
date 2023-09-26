# #from speech import recognizer
# from gtts import gTTS
# import os
# import numpy as np
# import librosa
# import soundfile
# import torch
# print('start')
# tts = gTTS('Testing testing testing ', tld='ca', slow=True)
# tts.save('hello.wav')
# #os.system('afplay ' + 'hello.mp3')
# print('hello')

# #print(torch.cuda.is_available())

# y, sr = librosa.load('hello.wav')
# new_y = librosa.effects.pitch_shift(y, sr=sr, n_steps=-7)
# soundfile.write("pitchShifted.wav", new_y, sr,)
# print('pitched')


import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('rate', 100) 
engine.setProperty('voice', voices[1].id)

r = sr.Recognizer()



#engine.say('<speak><prosody pitch="low" rate="slow" volume="loud">This is a test of SSML tags.</prosody></speak>')
#engine.runAndWait()

with sr.Microphone() as source:
    engine.say("Say something!")
    engine.runAndWait()
    print('listening')
    audio = r.listen(source)
print("speech done")

try:
    engine.say("Whisper thinks you said " + r.recognize_whisper(audio, language="english", model ="tiny.en"))
    engine.runAndWait()

except sr.UnknownValueError:
    engine.say("Whisper could not understand audio")
    engine.runAndWait()

except sr.RequestError as e:
    engine.say("Could not request results from Whisper")
    engine.runAndWait()



from langchain.llms import OpenAI

llm = OpenAI(openai_api_key="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")

