from pydub import AudioSegment

audio = AudioSegment.from_file("tts_sentences/thinking_sound.wav", format="mp3")
#audio2 = AudioSegment.from_file("tts_sentences/one_moment.wav", format="wav")

duration = len(audio)    
#trimmed_audio = audio[int(duration/44):int(duration/5)]
#silence = AudioSegment.silent(duration=1000)
#combined = audio2 + silence + audio1
trimmed_audio = audio - 10

trimmed_audio.export("tts_sentences/thinking_sound_quiet.wav", format="wav")