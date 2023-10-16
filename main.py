from ultralytics import YOLO
import serial
import cv2
#Initializes the face detection model
model = YOLO("Vision\Models\yolov8n-face.pt")
vid = cv2.VideoCapture(0)
#Need to do this aswell, because when its done once, the next time takes infinitely faster.
ret, img = vid.read()
results = model(img)
#Initalize servo motors.

#Just call another file?
body_parts    = ['B',   'P',    'T',     'S',      'E',   'G']
position_init = [1700,  1500,    2000,   2127.5,   1485,  1600] # E: 1650, S: 2200


#Call to motion detection, 

