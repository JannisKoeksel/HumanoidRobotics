from ultralytics import YOLO

import cv2

#Creates a model based on the pretrained data from the .pt file
model = YOLO("yolov8n-face.pt")
vid = cv2.VideoCapture(0)

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

    boxes = results[0].boxes
#Opens the image
#img = cv2.imread(img_path)
#Saves coordinates for the boxes and adds them onto the image
    for box in boxes:
        top_left_x = int(box.xyxy.tolist()[0][0])
        top_left_y = int(box.xyxy.tolist()[0][1])
        bottom_right_x = int(box.xyxy.tolist()[0][2])
        bottom_right_y = int(box.xyxy.tolist()[0][3])
        cv2.rectangle(img,(top_left_x, top_left_y), (bottom_right_x, bottom_right_y),(255,0,0),2)
#Write new image with boxes to specified folder.
#cv2.imwrite("TestResults.jpg", img)
# After the loop release the cap object
    cv2.imshow('frame', img)
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()