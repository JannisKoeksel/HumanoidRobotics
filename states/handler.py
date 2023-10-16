from .behavior import * 
from ..kinematics.hubert import move 
import time
import cv2

def idleHandler(state, stateData):
    return "initialized"


idle.add_handler(idleHandler)
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