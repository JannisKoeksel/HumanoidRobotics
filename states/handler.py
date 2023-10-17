from .state import StateMachine
import time
import cv2

import openai
import speech_recognition as sr

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


API_KEY = "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"




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
    print("Idle state started")
    
    
    # stateData.move("B", 80)
    # time.sleep(2)
    # stateData.move("B", -30)
    # time.sleep(2)
    # stateData.move("B", 30)
    # time.sleep(2)
    # stateData.move("B", -30)
    # time.sleep(2)
    # stateData.move("B", 30)
    # time.sleep(2)
    
    while True: 
        data = stateData.get()
        if( data["initialized"]): 
            return "initialized"
            


def scanHandler(state, stateData):
    staticBackground = None
    framesBetweenMovement = 500
    b = 1
    
    motion = 0
    sleep_time = 2
    a = 0

    while True:
        time.sleep(0.01)
        a += 1
        # Start of "scanning" behaviour
        data = stateData.get()
   
        frame = data["frame"]
        if (a % framesBetweenMovement == 0):
            staticBackground = None
            b += 1
            if (b % 2 == 1):
                #Move Body to middle
                stateData.move_servo('B',1700) 
            elif (b % 4):
                #Move Body to right/left
                stateData.move_servo('B',2100)
            else:
                stateData.move_servo('B',1300)
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



def faceDetectedHandler(state, stateData):
    timeToShowFace = 500
    timeToRecognizeFace = 500
    
    # Wait for a face to be detected
    for _ in range(timeToShowFace):
        data = stateData.get()
        if len(data["faces"]) > 0:
            # winsound.PlaySound("tts_sentences/found_you_processing_face.wav", winsound.SND_FILENAME)
            break

    # Try to recognize the detected face
    for _ in range(timeToRecognizeFace):
        data = stateData.get()
        for face in data["faces"].values():
            if face.label not in [None, -1]:
                filePath = f"tts_sentences/hello_{face.label}.wav"
                # winsound.PlaySound(filePath, winsound.SND_FILENAME)
                return "face_known"

    return "face_unknown"
        

def processPasswordHandler(state, stateData):
     #Add face tracking?
    n_attempts = 2
    attempts = 1
    while attempts <= n_attempts:

        with sr.Microphone() as source:
            if attempts == 1:
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
            if attempts == 1:
                winsound.PlaySound("tts_sentences/say_only_the_password,_nothing_else._i'll_give_you_one_more_try.wav", winsound.SND_FILENAME)
            else:
                winsound.PlaySound("tts_sentences/the_password_is_incorrect._acces_denied.wav", winsound.SND_FILENAME)

        else:
            if attempts == 1:
                winsound.PlaySound("tts_sentences/that's_not_the_password._i'll_give_you_one_more_try.wav", winsound.SND_FILENAME)
            else:
                winsound.PlaySound("tts_sentences/the_password_is_incorrect._acces_denied.wav", winsound.SND_FILENAME)
        
        attempts += 1
    return "pwd_wrong"



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

def follow(state, stateData):
    center_x, center_y = (240,320)
    while True: 
        time.sleep(0.05)
        print("___")
        data = stateData.get()
        faces = data["faces"]
        if(len(faces) ==  0): 
            stateData.move("B", 0)
            stateData.move("T", 0)
            continue
        
        
        face = list(faces.values())[0]
        if( not face.detected) : continue
        x, y = face.center[-1]
        
        tilt = center_x - x 
        body =  y - center_y
    
        print("body", body)
        print("tilt", tilt)
        
        if(body**2 > 300):
            stateData.move_delta("B", body/10)
        if(tilt**2 > 300):
            stateData.move_delta("T", tilt/10)

# StateMachine.add_handler("check_identity",check_identity_handler)
# StateMachine.add_handler("scanning",scanHandler)
# StateMachine.add_handler("idle",idleHandler)

def addHandlers():
    StateMachine.add_handler("check_identity",faceDetectedHandler)
    StateMachine.add_handler("scanning",follow)
    StateMachine.add_handler("idle",idleHandler)
    
    
    return StateMachine