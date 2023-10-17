from pydub import AudioSegment
import pyttsx3
import os


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 150) 
engine.setProperty('voice', voices[1].id)


def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms

def create_tts_sentence(sentence):
    folder = "tts_sentences/"
    filename = sentence.replace(" ", "_").lower() + "_untrimmed.wav"

    engine.save_to_file(sentence, filename)
    engine.runAndWait()

    audio = AudioSegment.from_file(filename, format="wav")

    start_trim = detect_leading_silence(audio)
    end_trim = detect_leading_silence(audio.reverse())
    duration = len(audio)    
    trimmed_audio = audio[start_trim:duration-end_trim]
    trimmed_audio.export(folder + sentence.replace(" ", "_").lower() + ".wav", format="wav")
    os.remove(filename)

create_tts_sentence("Access denied")


# Make function for creating a trimmmed sound_file out of a scentence
# Hubert listens for "hey hubert. "