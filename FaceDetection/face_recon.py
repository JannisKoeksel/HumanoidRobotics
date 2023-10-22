import face_recognition
import cv2
import numpy as np
import dlib
import time
import traceback



# Load a sample picture and create encodings.
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
    """
    Detects and recognizes faces in the provided frame using pre-known face encodings.

    This function resizes the given frame for faster processing, converts it to RGB, 
    and then detects face locations. It then extracts the face encodings and compares them 
    with known face encodings to recognize the individual. The function returns the recognized 
    label (name) of the face if a match is found, otherwise returns None.

    Parameters:
    - frame (numpy.ndarray): The frame in which to detect and recognize faces. It should be a BGR image 
                             as typically obtained from OpenCV functions.

    Globals:
    - known_face_encodings (list): List of face encodings for known individuals.
    - known_face_names (list): List of names corresponding to the known face encodings.

    Returns:
    - label (str or int): Name of the recognized individual, if a match is found. 
                          If no match is found or no faces are detected, it returns -1 or None.
    """
    h,w,d = frame.shape
    
    if(h > 300):
        small_frame = cv2.resize(frame, None, fx=0.25, fy=0.25)
    else: 
        small_frame = frame

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
    
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)

    face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations, model="large")

    label = None
    if(len(face_encodings) == 0): return label
    face_encoding = face_encodings[0]
    # See if the face is a match for the known face(s)
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)
    name = -1
    if matches[best_match_index]:
        distance = face_distances[best_match_index]
        if(distance < 0.6):
            name = known_face_names[best_match_index]

    label = name
    return label


def face_detect(queue_in,queue_out,terminate):
    """
    Processes frames from an input queue to detect faces and pushes the results to an output queue.

    This function continuously retrieves frames from the `queue_in`, applies face detection 
    using the `process_frame` function, and pushes the detection labels along with frame IDs 
    to the `queue_out`. The processing runs continuously until the `terminate` flag is set.

    Parameters:
    - queue_in (multiprocessing.Queue): An input queue to retrieve frames and frame IDs.
    - queue_out (multiprocessing.Queue): An output queue to push the detection labels and frame IDs.
    - terminate (multiprocessing.Value): A flag to control the termination of the processing loop.
        If set to 1, the processing stops.

    Outputs to queue_out:
    - labels (list): List of detected face labels for each frame.
    - frame_id (int): ID of the frame corresponding to the labels.

    Note:
    The function assumes the availability of a `process_frame` function for detecting faces in a frame.
    Ensure that the terminate flag is initialized to 0 for the function to start. To stop the function,
    set the terminate flag to 1. The provided input queue should contain frames and frame IDs, 
    and the output queue should be used to retrieve the processed labels and frame IDs.

    Returns:
    None

    Raises:
    Exception: If there's an error during the processing.
    """
    try:
        while True:
            time.sleep(0.001)
            if(terminate.value == 1):
                break
            # time.sleep(0.01)
            latest_data = None
            while True:
                try:
                    latest_data = queue_in.get(False)
                    # print("q",latest_data["frame_id"])
                except:
                    break
            
            if(latest_data == None):
                continue
            
            frames = latest_data["frames"]
            frame_id = latest_data["frame_id"]
                
            labels = []
            # print("recognition frames:", len(frames))
            for frame in frames: 
                label = process_frame(frame)
                labels.append(label)
            # print("recognition labels:", len(labels))
            # print("recognition frame id", frame_id)
            queue_out.put({"labels":labels, "frame_id":frame_id})
    except Exception as e:
        print("recognition",e)
        print(traceback.format_exc())