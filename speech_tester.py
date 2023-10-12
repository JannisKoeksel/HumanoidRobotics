# from speech import recognizer
from pydub import AudioSegment
import openai
import speech_recognition as sr
import pyttsx3
import time
import threading
import winsound
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain

API_KEY = "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"

def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms

def create_current_message(sentence):
    filename = "current_message.wav"

    engine.save_to_file(sentence, filename)
    engine.runAndWait()

    audio = AudioSegment.from_file(filename, format="wav")

    start_trim = detect_leading_silence(audio)
    end_trim = detect_leading_silence(audio.reverse())
    duration = len(audio)    
    trimmed_audio = audio[start_trim:duration-end_trim]
    trimmed_audio.export("current_message.wav", format="wav")

engine = pyttsx3.init()
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('rate', 150) 
engine.setProperty('voice', voices[1].id)

chat = ChatOpenAI(openai_api_key=API_KEY, model_name="gpt-3.5-turbo", temperature=0.9)

prompt = ChatPromptTemplate(
    input_variables=['user', 'chat_history', 'question'],
    messages=[
        SystemMessagePromptTemplate.from_template(
            "You are a guard robot named Hubert with the purpose of surveilling Area 51. You are talking to {user} who is authorized personnel. The conversation started by you asking {user} how they are doing."
        ),
        # The `variable_name` here is what must align with memory
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
)
memory = ConversationBufferMemory(memory_key="chat_history", input_key='question', return_messages=True)

conv = LLMChain(
    llm=chat,
    prompt=prompt,
    memory=memory
)

n_questions = 3
max_questions = 2

username = "Kevin"

#engine.say(f"Hello {username}, how is it going?")
#engine.runAndWait()

create_current_message(f"Hello {username}, how is it going?")
target=winsound.PlaySound("current_message.wav", winsound.SND_FILENAME)

while n_questions < max_questions:

    with sr.Microphone() as source:
        print('listening')
        winsound.Beep(1000,100)
        audio = sr.Recognizer().listen(source)
    start= time.time()

    audio_thread = threading.Thread(target=winsound.PlaySound, args=("tts_sentences/thinking_sound_quiet.wav", winsound.SND_FILENAME,))
    audio_thread.start()
    wav_data = audio.get_wav_data()
    with open('output.wav', 'wb') as f:
        f.write(wav_data)
    audio_file= open("output.wav", "rb")

    transcript = openai.Audio.transcribe("whisper-1", audio_file, api_key=API_KEY)
    print(transcript['text'])

    result = conv.predict(question=transcript['text'], user=username)

    end = time.time()
    print('Whisper + ChatGPT time: ' + str(end - start))
    audio_thread.join()

    print(result)
    #engine.say(result)
    #engine.runAndWait()
    create_current_message(result)
    target=winsound.PlaySound("current_message.wav", winsound.SND_FILENAME,)

    n_questions += 1

winsound.PlaySound("tts_sentences/hold_on,_i_need_to_get_back_to_work._goodbye!.wav", winsound.SND_FILENAME)

# r = sr.Recognizer()
# with sr.Microphone() as source:
#     print('listening')
#     audio = r.listen(source)

# #audio_thread.start()
# wav_data = audio.get_wav_data()

# with open('output.wav', 'wb') as f:
#     f.write(wav_data)
# audio_file= open("output.wav", "rb")

# transcript = openai.Audio.transcribe("whisper-1", audio_file, api_key=API_KEY)
# print(transcript['text'])

# result = conv.predict(question=transcript['text'], user="Kevin")
# print(result)
# engine.say(result)
# engine.runAndWait()

