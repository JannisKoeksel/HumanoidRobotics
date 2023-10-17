from .state import StateMachine
import time
import cv2

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