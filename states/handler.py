from .behavior import * 
from ..kinematics.hubert import move,sikta,shoot
from ..kinematics.faceTracking import faceTracking
import time
import cv2
import winsound
import numpy as np
from pydub import AudioSegment
import openai
import speech_recognition as sr
import pyttsx3
import threading
import winsound
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
#from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from ..speech.speech_handler_function import create_current_message, detect_leading_silence


API_KEY = "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"

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 150) 
engine.setProperty('voice', voices[1].id)

chat = ChatOpenAI(openai_api_key=API_KEY, model_name="gpt-3.5-turbo", temperature=0.9)

prompt = ChatPromptTemplate(
    input_variables=['user', 'chat_history', 'question'],
    messages=[
        SystemMessagePromptTemplate.from_template(
            "You are a guard robot named Hubert with the purpose of surveilling Area 51. You are talking to {user} who is authorized personnel. The conversation started by you asking {user} how they are doing. You always answer in English regardless of what language a question was told."
        ),
        # The `variable_name` here is what must align with memory
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
)
memory = ConversationBufferMemory(memory_key="chat_history", input_key='question', return_messages=True)

conv_chain = LLMChain(
    llm=chat,
    prompt=prompt,
    memory=memory
)


def idleHandler(state, stateData):
    return "initialized"


idle.add_handler(idleHandler)

def scanHandler(state, stateData):
    staticBackground = None
    framesBetweenMovement = 200
    b = 1
    motion = 0
    sleep_time = 2
    a = 0
    while True:
        time.sleep(0.01)
        a += 1
        # Start of "scanning" behaviour
        data = stateData.get()
        frame = data["frame"].values()
        if (a % framesBetweenMovement == 0):
            staticBackground = None
            b += 1
            if (b % 2 == 1):
                #Move Body to middle
                move('B',1700) 
            elif (b % 4):
                #Move Body to right/left
                move('B',2100)
            else:
                move('B',1300)
            #Get some better function here
            #We want the movement to finish so measure the time it takes
            #For Hubert to move into each position.
            time.sleep(sleep_time)
            #Reads frame and check condition
            #Increments frame number
            # Initializing motion = 0 (no motion)        # Converting color image to gray scale image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #Apply gaussianblur on the grayscaled image
            # so that change can be found easily
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

            #Assign background image as the first frame
        if staticBackground is None:
            staticBackground = gray
            continue
            #Calculates the difference between current frame and background frame
        diffFrame = cv2.absdiff(staticBackground, gray)

            
            #The motion sensitivity, a greater value is less sensitive
        motionSensitivity = 35

            # If change in between static background and
            # current frame is greater than motionSensitivity it will show white color(255)
        threshFrame = cv2.threshold(diffFrame, motionSensitivity, 255, cv2.THRESH_BINARY)[1]
            #Dilates any motion found to easier find contour, may be unnecessary for our purposes
        threshFrame = cv2.dilate(threshFrame, None, iterations=2)

            # Finding contour of moving object
        conts, _ = cv2.findContours(threshFrame.copy(),
                                    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in conts:
            if cv2.contourArea(contour) < 10000:
                continue
            return "motion"

scanning.add_handler(scanHandler)

def faceDetectedHandler(state, stateData):
    timeToShowFace = 3
    timeToRecognizeFace = 5
    detected = False
    winsound.PlaySound("tts_sentences/show_yourself.wav", winsound.SND_FILENAME)
    time1 = np.datetime64('now')
    diff = 0
    while (diff < timeToShowFace):
        time2 = np.datetime64('now')
        diff = (np.datetime64(time2)-np.datetime64(time1))/(np.timedelta64(1,'s'))
        #for i in range(timeToShowFace):
        data = stateData.get()
        if len(data["faces"]) > 0:
          detected = True
          winsound.PlaySound("tts_sentences/found_you.wav", winsound.SND_FILENAME)
          winsound.PlaySound("tts_sentences/processing_face.wav", winsound.SND_FILENAME)
          break
    if detected == False:
        return "no_face"
    diff = 0
    time1 = np.datetime64('now')
    while (diff < timeToRecognizeFace):
      time2 = np.datetime64('now')
      diff = (np.datetime64(time2)-np.datetime64(time1))/(np.timedelta64(1,'s'))
      data = stateData.get()
      for face in data["faces"].values():
          if face.label not in [None, -1]:
              filePath = f"tts_sentences/hello_{face.label}.wav"
              winsound.PlaySound(filePath, winsound.SND_FILENAME)
              return "face_known"
    return "face_unknown"
          
check_identity.add_handler(faceDetectedHandler)
#Not needed below?
#def fightHandler(state, stateData):
#    timeToShoot = 3
    #winsound.Playsound("tts_sentences/access_denied.wav", winsound.SND_FILENAME)
#    time.sleep(timeToShoot)
    #winsound.Playsound("tts_sentences/shoot.wav",winsound.SND_FILENAME)
def defendHandler(state, stateData):
    winsound.PlaySound("tts_sentences/you_have_5_seconds_to_leave_the_area.wav", winsound.SND_FILENAME)
    #time_stamp_start
    sikta()
    timeToLeave = 5
    time1 = np.datetime64('now')
    diff = 0
    while (diff < timeToLeave):
        time2 = np.datetime64('now')
        diff = (np.datetime64(time2)-np.datetime64(time1))/(np.timedelta64(1,'s'))
        data = stateData.get()
        faces = data["faces"].values()

        position = data["position"].values()
        bodyPos = position.bodyPos
        #update body and headpos
        #If hubert can follow the movement altogether
        if bodyPos > 2300 or bodyPos < 600:
            return "person_leaves" 
        #If the person is moving a bit too quickly
        elif len(faces == 0):
            return "person_leaves"
    shoot()
    time.sleep(5)
    return "person_leaves"
defend.add_handler(defendHandler)

def processPasswordHandler(state, stateData):
     #Add face tracking?
    n_attemps = 2
    attemps = 1
    while attemps <= n_attemps:

        with sr.Microphone() as source:
            if attemps == 1:
                winsound.PlaySound("tts_sentences/say_the_super_secret_password.wav", winsound.SND_FILENAME)
            winsound.Beep(1000,100)
            audio = sr.Recognizer().listen(source)
        print("speech done")

        wav_data = audio.get_wav_data()
        with open('output.wav', 'wb') as f:
            f.write(wav_data)
        audio_file= open("output.wav", "rb")

        transcript = openai.Audio.transcribe("whisper-1", audio_file, api_key=API_KEY)
        print(transcript['text'])
        results = transcript['text']

        if results.lower().replace(" ", "").replace(".", "") == "banana":
            winsound.PlaySound("tts_sentences/acces_granted._welcome.wav", winsound.SND_FILENAME)
            return "pwd_correct"
    
        elif "banana" in results.lower():
            if attemps == 1:
                winsound.PlaySound("tts_sentences/say_only_the_password,_nothing_else._i'll_give_you_one_more_try.wav", winsound.SND_FILENAME)
            else:
                winsound.PlaySound("tts_sentences/the_password_is_incorrect._acces_denied.wav", winsound.SND_FILENAME)

        else:
            if attemps == 1:
                winsound.PlaySound("tts_sentences/that's_not_the_password._i'll_give_you_one_more_try.wav", winsound.SND_FILENAME)
            else:
                winsound.PlaySound("tts_sentences/the_password_is_incorrect._acces_denied.wav", winsound.SND_FILENAME)
        
        attemps += 1
    return "pwd_wrong"
process_pwd.add_handler(processPasswordHandler)


def entryApprovedHandler(state, stateData):

    username = "human" #a human
    data = stateData.get()
    faces = data["faces"].values()
    if 0 < len(faces):
        if faces[0] not in [-1, None]:
            username = faces[0].label

    if username == "human":
        system_message = "You are a guard robot named Hubert with the purpose of surveilling Area 51. " \
                         "You are talking to a {user} who is authorized personnel. " \
                         "The conversation started by you asking the {user} how they are doing. " \
                         "You always answer in English regardless of what language a question was told."
    else:
        system_message = "You are a guard robot named Hubert with the purpose of surveilling Area 51. " \
                         "You are talking to {user} who is authorized personnel. " \
                         "The conversation started by you asking {user} how they are doing. " \
                         "You always answer in English regardless of what language a question was told."

    prompt = ChatPromptTemplate(
        input_variables=['user', 'chat_history', 'question'],
        messages=[
            SystemMessagePromptTemplate.from_template(system_message),
            # The `variable_name` here is what must align with memory
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{question}")
        ]
    )
    memory = ConversationBufferMemory(memory_key="chat_history", input_key='question', return_messages=True)

    conv_chain = LLMChain(
        llm=chat,
        prompt=prompt,
        memory=memory
    )

    n_questions = 0 #Should be 0
    max_questions = 2

    create_current_message(f"Hello {username}, how is it going?")
    winsound.PlaySound("current_message.wav", winsound.SND_FILENAME)

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

        result = conv_chain.predict(question=transcript['text'], user=username)

        end = time.time()
        print('Whisper + ChatGPT time: ' + str(end - start))
        audio_thread.join()

        print(result)
        #engine.say(result)
        #engine.runAndWait()
        create_current_message(result)
        winsound.PlaySound("current_message.wav", winsound.SND_FILENAME,)

        n_questions += 1

    winsound.PlaySound("tts_sentences/hold_on._i_should_acctually_get_back_to_work._goodbye.wav", winsound.SND_FILENAME)
    return "waiting_for_entry"
entry_approved.add_handler(entryApprovedHandler)
