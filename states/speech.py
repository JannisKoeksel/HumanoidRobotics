

import pyttsx3
from pydub import AudioSegment

def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
    """
    Detects the duration (in milliseconds) of leading silence in an audio segment.

    Parameters:
    - sound (AudioSegment): The audio segment for which leading silence needs to be detected.
    - silence_threshold (float, optional): The dBFS (decibels relative to full scale) value below which 
      the audio is considered silent. Default is -50.0 dBFS.
    - chunk_size (int, optional): The duration (in milliseconds) of audio chunks to be checked for silence. 
      Default is 10 milliseconds.

    Returns:
    - int: The duration (in milliseconds) of leading silence.

    The function iterates through the audio segment in chunks and detects the point where the sound level 
    exceeds the silence threshold, indicating the end of the silence.

    Note:
    This function uses the 'pydub' library and works with AudioSegment objects. The returned duration can be 
    used for trimming purposes.
    """
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms

def create_current_message(sentence):
    """
    Generates and saves an audio message using text-to-speech conversion for a given sentence.

    Parameters:
    - sentence (str): The text that needs to be converted to speech.

    The generated audio message will have leading and trailing silence trimmed and will be saved 
    as 'current_message.wav'. The function uses the 'pyttsx3' library for text-to-speech conversion 
    and 'pydub' for audio processing.

    Note: 
    The text-to-speech conversion uses the second available voice and a rate of 150 for speech speed. 
    The saved audio message will overwrite the previous 'current_message.wav', if it exists.
    """
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 150) 
    engine.setProperty('voice', voices[1].id)
    
    filename = "current_message.wav"

    engine.save_to_file(sentence, filename)
    engine.runAndWait()

    audio = AudioSegment.from_file(filename, format="wav")

    start_trim = detect_leading_silence(audio)
    end_trim = detect_leading_silence(audio.reverse())
    duration = len(audio)    
    trimmed_audio = audio[start_trim:duration-end_trim]
    trimmed_audio.export("current_message.wav", format="wav")