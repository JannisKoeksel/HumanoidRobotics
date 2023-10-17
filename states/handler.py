from .state import StateMachine
import time
import cv2
import numpy as np
import openai
import speech_recognition as sr
from .functionality import *
import threading
import winsound



from .speech import create_current_message


def idleHandler(state, stateData):
    print("Idle state started")
    
    stateData.move("S",0)
    stateData.move("E",5)
    stateData.move_servo("G",1390)
    
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
    stateData.move('B',0) 
    motion = 0
    sleep_time = 2
    a = 0
    stateData.should_follow = False
    stateData.wait(5)
    while True:
 
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
            stateData.wait(5)
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
            stateData.should_follow = True
            return "motion"


def DetectFacesHandler(state, stateData):
    stateData.wait(5)
    data = stateData.get()
    
    if(list(data["faces"].values()) == 0):
        winsound.PlaySound("tts_sentences/show_yourself.wav", winsound.SND_FILENAME)
    
    detected = faceDetectionHandler_check_for_face(stateData)
    if not detected :
        return "no_face"
    
    recognized = faceDetectionHandler_recognized_face(stateData)
    
    if(recognized):
        
        return "face_known"
    
    return "face_unknown"
        

def processPasswordHandler(state, stateData):
    
    n_attempts = 2
    attempts = 1
    while attempts <= n_attempts:
        print("PWD attempt", attempts, "start")
        
        if attempts == 1:
            winsound.PlaySound("tts_sentences/say_the_super_secret_password.wav", winsound.SND_FILENAME)
        
        audio = general_speech_detection()
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
    print("entry approved")
    
    username = processPasswordHandler_get_username(stateData)
    conv_chain = processPasswordHandler_lang_setup(username)

    create_current_message(f"Hello {username}, how is it going?")
    winsound.PlaySound("current_message.wav", winsound.SND_FILENAME)

    n_questions = 0 #Should be 0
    max_questions = 2
    
    while n_questions < max_questions:
        start = time.time()
        
        #play waiting sound
        play_audio_thread = threading.Thread(target=winsound.PlaySound, args=("tts_sounds/thinking_sound_quiet.wav", winsound.SND_FILENAME,))
        play_audio_thread.start()
        
        # record microphone
        audio = general_speech_detection()
        wav_data = audio.get_wav_data()
        
        # save audio file 
        with open('output.wav', 'wb') as f:
            f.write(wav_data)
        audio_file= open("output.wav", "rb")

        # transcribe audio file
        transcript = openai.Audio.transcribe("whisper-1", audio_file, api_key=API_KEY)
        print(transcript['text'])

        # run langchain
        result = conv_chain.predict(question=transcript['text'], user=username)

        end = time.time()
        print('Whisper + ChatGPT time: ' + str(end - start))
        print(result)
        
        # answer question
        create_current_message(result)
        winsound.PlaySound("current_message.wav", winsound.SND_FILENAME,)
        
        n_questions += 1
        play_audio_thread.join()

    #easter egg
    stateData.wait(1)
    winsound.PlaySound("tts_sentences/hold_on._i_should_acctually_get_back_to_work._goodbye.wav", winsound.SND_FILENAME)
    
    stateData.wait(10)
    return "waiting_for_entry"


def defendHandler(state, stateData):
    
    stateData.wait(5)
    
    
    winsound.PlaySound("tts_sentences/you_have_20_seconds_to_leave_the_area.wav", winsound.SND_FILENAME)
   
    #pull gun 
    stateData.move_servo('E', 2050)
    stateData.wait(1)
    stateData.move_servo('S', 1750)
    
    
    is_gone = defendHandler_pearson_has_left(stateData)
    
    if not is_gone:
        stateData.move_servo('G', 1700)
        
        play_audio_thread = threading.Thread(target=defendHandler_shoot_sound)
        play_audio_thread.start()
        
        
        stateData.wait(13)
        
        play_audio_thread.join()
    
    else:
        stateData.wait(8)
        
        
    return "person_leaves"


def addHandlers():
    StateMachine.add_handler("idle",idleHandler)
    StateMachine.add_handler("scanning",scanHandler)
    StateMachine.add_handler("defend", defendHandler)
    StateMachine.add_handler("process_pwd", processPasswordHandler)
    StateMachine.add_handler("check_identity",DetectFacesHandler)
    StateMachine.add_handler("entry_approved",entryApprovedHandler)
    
    # StateMachine.add_handler("entry_forbidden")

    
    return StateMachine