from ultralytics import YOLO

import cv2

#Creates a model based on the pretrained data from the .pt file
model = YOLO("Vision\Models\yolov8n-face.pt")
#Pretrained model acquired from https://github.com/akanametov/yolov8-face
vid = cv2.VideoCapture(1)
#May have to change center Image depending on the resolution of Hubert's camera.
centerImage = [320,240]
while (True):
#Image path to the test picture
#img_path = "FaceTest.jpg"
#Apply model on the image and saves the results (Coordinates for rectangles)
    ret, img = vid.read()

# the 'q' button is set as the
# quitting button you may use any
# desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    results = model(img)
#Info about the detected faces are found in boxes.
    boxes = results[0].boxes
#Opens the image
#img = cv2.imread(img_path)
#Saves coordinates for the boxes and adds them onto the image
    a = 1
    for box in boxes:
        #Extracting coordinates of detected faces
        topLeftX = int(box.xyxy.tolist()[0][0])
        topLeftY = int(box.xyxy.tolist()[0][1])
        bottomRightX = int(box.xyxy.tolist()[0][2])
        bottomRightY = int(box.xyxy.tolist()[0][3])
        if (a == 1):
            #Send the difference between the center of the rectangle encapsulating the first face and the center of the image 
            #to Arduino with a scale factor, should make the robot track the faces. However, may have to make it so it only 
            #sends it to Arduino every X frames so it doesnt have a seizure, also scale factor could be important.
            centerFaceCoords = [(topLeftX + bottomRightX )/2, (topLeftY + bottomRightY)/2]
            diffX = centerFaceCoords[0] - centerImage[0]
            diffY = centerFaceCoords[1] - centerImage[1]
        cv2.rectangle(img,(topLeftX, topLeftY), (bottomRightX, bottomRightY),(255,0,0),2)
        a = a + 1
#Write new image with boxes to specified folder.
#cv2.imwrite("TestResults.jpg", img)
# After the loop release the cap object
    cv2.imshow('frame', img)
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()