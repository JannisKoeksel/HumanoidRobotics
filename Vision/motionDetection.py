# Python program to implement
# Webcam Motion Detector
#Code acquired from https://www.geeksforgeeks.org/webcam-motion-detector-python/
import sys
# importing OpenCV
import cv2
import time
#Add some idle behaviour?? Move Hubert Body from left to right...
# Assigning our static_back to None
#def motion_detection(queue, terminate):
    #Initializes the background
    # Capturing video
    #Note that the argument should be different when connecting to the Hubert camera, camera -> argument=1 
video = cv2.VideoCapture(1)
    #Counts frames, use this one to make changes every X frames.
def motionLoop(nFrames, frame):
    staticBackground = None
    framesBetweenMovement = 200
    b = 1
    motion = 0
    while motion == 0:
            # Start of "scanning" behaviour
        if (nFrames % framesBetweenMovement == 0):
            staticBackground = None
            b += 1
            if (b % 2 == 1):
                #Function calls, just pseudo coded right now.
                moveBodyPos(1700) 
            elif (b % 4):
                moveBodyPos(2100)
            else:
                moveBodyPos(1300)
            #Get some better function here
            #We want the movement to finish so measure the time it takes
            #For Hubert to move into each position.
            time.sleep(10)
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
            motion = 1
                #Adds a rectangle to motion found. Probably unnecessary for our purposes, but good for testing.
                #(x, y, w, h) = cv2.boundingRect(contour)
                # making green rectangle around the moving object
                #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

            # Displaying image in gray_scale
            #cv2.imshow("Gray Frame", gray)

            # Displaying the difference in currentframe to
            # the staticframe(very first_frame)
            #cv2.imshow("Difference Frame", diff_frame)

            # Displaying the black and white image in which if
            # intensity difference greater than 30 it will appear white
            #cv2.imshow("Threshold Frame", thresh_frame)

            # Displaying color frame with contour of motion of object
            #cv2.imshow("Color Frame", frame)

            # Terminate if needed or add to queue, (probably not needed aswell.)
            # Destroying all the window
        #Transition state
