import face_recognition
import cv2
import numpy as np
import dlib
import time


# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
# video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
jannis_image = face_recognition.load_image_file("D:/IT/HumanoidRobotics/FaceDetection/faces/jannis.jpg")
jannis_face_encoding = face_recognition.face_encodings(jannis_image)[0]
emma_image = face_recognition.load_image_file("D:/IT/HumanoidRobotics/FaceDetection/faces/emma.jpg")
emma_face_encoding = face_recognition.face_encodings(emma_image)[0]
kevin_image = face_recognition.load_image_file("D:/IT/HumanoidRobotics/FaceDetection/faces/kevin.jpg")
kevin_face_encoding = face_recognition.face_encodings(kevin_image)[0]


# Create arrays of known face encodings and their names
known_face_encodings = [
    jannis_face_encoding,
    emma_face_encoding,
    kevin_face_encoding
]
known_face_names = [
    "Jannis",
    "Emma",
    "Kevin"
]


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


def process_frame(frame):
    # Resize frame of video to 1/4 size for faster face recognition processing
    
    h,w,d = frame.shape
    
    if(h > 300):
        small_frame = cv2.resize(frame, None, fx=0.25, fy=0.25)
    else: 
        small_frame = frame

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
    
    # print("before face_locations")
    # print(type(rgb_small_frame), rgb_small_frame.shape, rgb_small_frame.dtype)

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    # print(face_locations)
    
  

    face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations, model="small")


    label = "Unknown"
    if(len(face_encodings) == 0): return label
    face_encoding = face_encodings[0]
    # See if the face is a match for the known face(s)
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)


    # # If a match was found in known_face_encodings, just use the first one.
    # if True in matches:
    #     first_match_index = matches.index(True)
    #     name = known_face_names[first_match_index]

    # Or instead, use the known face with the smallest distance to the new face
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        name = known_face_names[best_match_index]

    label = name
    return label


def face_detect(queue_in,queue_out,terminate):
    while True:
        if(terminate.value == 1):
            break
        time.sleep(0.01)
        latest_data = None
        while not queue_in.empty():
            latest_data = queue_in.get()
        
        if(latest_data == None):
            continue
        
        frames = latest_data["frames"]
            
            
        labels = []
        
        for frame in frames: 
            label = process_frame(frame)
            labels.append(label)

        queue_out.put(labels)