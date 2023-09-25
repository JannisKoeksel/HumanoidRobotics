# Python program to implement
# Webcam Motion Detector

# importing OpenCV
import cv2

# Assigning our static_back to None
staticBackground = None

# Capturing video
#Note that the argument should be different when connecting to the Hubert camera, 
video = cv2.VideoCapture(0)

# Infinite while loop to treat stack of image as video
#May want to change this to see the difference between the current frame and the frame x frames before
#Instead of the difference between the current frame and the "base" frame.
while True:
    # Reading frame(image) from video
    check, frame = video.read()

    # Initializing motion = 0 (no motion)
    motion = 0

    # Converting color image to gray_scale image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Converting gray scale image to GaussianBlur
    # so that change can be found easily
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # In first iteration we assign the value
    # of static_back to our first frame
    if staticBackground is None:
        staticBackground = gray
        continue

    # Difference between static background
    # and current frame(which is GaussianBlur)
    diffFrame = cv2.absdiff(staticBackground, gray)

    # If change in between static background and
    # current frame is greater than 30 it will show white color(255)
    #The motion sensitivity, a greater value is less sensitive
    motionSensitivity = 35
    threshFrame = cv2.threshold(diffFrame, motionSensitivity, 255, cv2.THRESH_BINARY)[1]
    threshFrame = cv2.dilate(threshFrame, None, iterations=2)

    # Finding contour of moving object
    cnts, _ = cv2.findContours(threshFrame.copy(),
                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        motion = 1
        #Add a statement to for transition between states, that is motion is detected -> "show your face" -> face detection
        (x, y, w, h) = cv2.boundingRect(contour)
        # making green rectangle around the moving object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # Displaying image in gray_scale
    #cv2.imshow("Gray Frame", gray)

    # Displaying the difference in currentframe to
    # the staticframe(very first_frame)
    #cv2.imshow("Difference Frame", diff_frame)

    # Displaying the black and white image in which if
    # intensity difference greater than 30 it will appear white
    #cv2.imshow("Threshold Frame", thresh_frame)

    # Displaying color frame with contour of motion of object
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)
    # if q entered whole process will stop
    if key == ord('q'):
        break

video.release()

# Destroying all the windows
cv2.destroyAllWindows()
