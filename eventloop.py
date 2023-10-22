import multiprocessing
from vision import face_detection
from FaceDetection import face_detect as identify_faces
from FaceDetection.face_recon import process_frame
import cv2
import time
from dataclasses import dataclass
from typing import Tuple, List, Dict
import traceback


DISTANCE_THRESHOLD = 40
MAX_AGE_THRESHOLD = 50
MIN_AGE_THRESHOLD = 10
MAX_AGE_FOR_DETECTION = 2


old_face_locs = None

def get_center_point(face_coords):
    x = (face_coords[0]+face_coords[2])/2.
    y = (face_coords[1]+face_coords[3])/2.
    
    return x,y


def euclidean_distance(x,y,old_x,old_y):
    return ((x-old_x)**2 + (y-old_y)**2)**0.5

@dataclass
class Face: 
    """
    Dataclass to represent a detected face.

    Attributes:
    - center: List of tuples containing x, y coordinates of the face center over time.
    - label: Identifier or name associated with the detected face. Can be a string, integer, or None.
    - fid: A unique face ID.
    - age: Age of the face in terms of frames since it was first detected.
    - frame: List of frame numbers where the face was detected.
    - detections: Number of times this face has been detected.
    - detected: Flag to indicate if the face has been successfully labeled/detected.
    """
    
    center: List[Tuple[int,int]]
    label: str|None|int
    fid: int
    age:int 
    frame: List[int]
    detections = 0
    detected = False
    
    def update_center(self,x:int,y:int):
        """
        Update the center coordinates of the detected face.

        Args:
        x (int): The x-coordinate of the center.
        y (int): The y-coordinate of the center.

        Raises:
        None

        Returns:
        None

        Notes:
        Maintains the size of the 'center' list by removing older points if the number of stored points exceeds
        (MAX_AGE_THRESHOLD * 4). Specifically, the oldest (MAX_AGE_THRESHOLD * 3) points are deleted.
        """
        if(len(self.center) > MAX_AGE_THRESHOLD*4):
            del self.center[0:MAX_AGE_THRESHOLD*3]
            
        self.center.append((x,y))
        
    def update_label(self,label:str|int|None):
        """
        Update the label of the face with the provided label.

        Args:
            label (Union[str, int, None]): The label to update with. Can be a string, integer, or None.

        Raises:
            None

        Returns:
            None

        Notes:
            If the current label is None or -1 and a valid label is provided, the face's label is updated.
            Additionally, if a valid label (other than None or -1) is provided, the 'detected' attribute of the face is set to True.
        """
        # self.label = label
        if(label == None): return
        
        if(self.label == None or self.label == -1):
            self.label = label
        
        if(label != None and label != -1):
            self.detected = True    
        
            
    def get_distance(self,x:int,y:int):
        """
        Calculate the Euclidean distance between a provided point and the latest center of the detected face.

        Args:
        x (int): The x-coordinate of the given point.
        y (int): The y-coordinate of the given point.

        Raises:
        None

        Returns:
        float: The Euclidean distance between the two points.

        Notes:
        Uses the 'euclidean_distance' function to compute the distance.
        The latest center of the detected face is retrieved from the end of the 'center' list.
        """
        return euclidean_distance(x,y,*self.center[-1])
    
    
class FaceData:
    frame_id = 0
    face_id = 0
    historic_data = {}
    
    def __init__(self):
        self.faces: Dict[int, 'Face'] = {}
    
    def get_id_if_exists(self, x,y):
        """
        Determine if a face already exists near the given point (x,y).

        This method checks the distance of the given point (x,y) to the center of previously detected faces.
        If a face is found within the DISTANCE_THRESHOLD, its ID is returned. If no such face is found, None is returned.

        Args:
        x (int): The x-coordinate of the point.
        y (int): The y-coordinate of the point.

        Returns:
        Optional[int]: The ID of the existing face within the threshold, or None if no such face exists.
        """
        if(len(self.faces.keys()) == 0):return None
        min_distance = 1000
        min_d_fid = None
        for old_face in self.faces.values():
            distance = old_face.get_distance(x,y)
            if(distance < min_distance and distance < DISTANCE_THRESHOLD):
                min_distance = distance
                min_d_fid = old_face.fid
                
        return min_d_fid
    
    def process_new_frame(self, face_locations, face_labels, labels_frame_id):
        """
        Process a new frame to update and manage detected face data.

        This method carries out the following operations:
        1. Ages each previously detected face by increasing its age counter.
        2. Identifies and marks faces for deletion if they exceed the `MAX_AGE_THRESHOLD`.
        3. Checks for duplicate labels and removes duplicates.
        4. Processes new face locations to determine if they match existing faces or if they are new detections.
        5. Updates or adds face records accordingly.
        6. If labels are provided for the detected faces, they are associated with the corresponding face records.
        7. Updates the historic data with the IDs of the faces detected in the current frame.

        Args:
            face_locations (List[Tuple[int, int, int, int]]): A list of face locations represented as (top, right, bottom, left) coordinates.
            face_labels (List[Union[str, int, None]]): A list of labels for the detected faces.
            labels_frame_id (int): The frame ID associated with the provided face labels.

        Raises:
            Exception: If there's a mismatch in the length of historic data and face labels.
        """
        # print("process frame", face_locations)
        #update data age
        to_delete = []
        for key in self.faces.keys():
            old_face = self.faces[key]
            old_face.age += 1
            if(old_face.age > MAX_AGE_THRESHOLD):
                to_delete.append(key)
                
            
            if(old_face.detections > MIN_AGE_THRESHOLD):
                old_face.detected = True
                
                
            if(old_face.age > MAX_AGE_FOR_DETECTION):
                old_face.detected = False
                
        #kill old 
        for key in to_delete: 
            self.faces.pop(key)
            
        #check for duplicates 
        labels = set()
        to_delete = set()
        for key in self.faces.keys():
            face = self.faces[key]
            label = face.label
            if(label in labels):
                to_delete.add(label)
            
            if(label != -1 and label != None):
                labels.add(label)
            
        for key in self.faces.keys():
            face = self.faces[key]
            label = face.label
            if(label in to_delete):
                face.label = None
        
        face_ids = []
        # process 
        for face_loc in face_locations:
            x,y = get_center_point(face_loc)
                
            fid = self.get_id_if_exists(x,y)
            
            if(fid == None):
                fid = self.face_id
                self.face_id += 1
                face = Face([(x,y)], None, fid, 0, face_loc)
                self.faces[fid] = face
                face_ids.append(fid)
            else:
                self.faces[fid].update_center(x,y)
                # self.faces[fid].update_label(label)
                self.faces[fid].age = 0
                self.faces[fid].detections += 1
                self.faces[fid].frame = face_loc
                face_ids.append(fid)
                
        self.historic_data[self.frame_id] = face_ids
        
        
        if(face_labels != None):
            historic_data = self.historic_data[labels_frame_id]
            if(len(historic_data) != len(face_labels)):
                print("len missmatch")
            for i,fid in enumerate(historic_data): 
                try:
                    self.faces[fid].update_label(face_labels[i])
                except: 
                    print("historic data key missmatch")
                    print("h data", historic_data)
                    print(face_labels)
                    for key in self.faces.keys():
                        print(str(key) + ", ", end="")
                        print()
                    print("Frame id", self.frame_id, "historic id ", labels_frame_id)

        self.frame_id += 1


def start(queue, quit):
    """
    Start the main event loop to manage face detection and recognition processes.

    The function initializes two parallel processes: 
    1. `face_detection` - Responsible for detecting faces in frames.
    2. `identify_faces` - Responsible for identifying recognized faces based on previous data.
    
    The function continuously processes frames, updates the detected faces data, and communicates 
    with the parallel processes using multiprocessing queues.

    Args:
        queue (multiprocessing.Queue): The main data queue used to gather and send out data.
        quit (multiprocessing.Value): A flag to indicate when to exit the event loop and terminate the processes.

    Raises:
        Exception: Captures and prints any exception that occurs within the event loop.
    """
    print("starting eventloop")
    face_data = FaceData()

    face_queue = multiprocessing.Queue()
    face_quit = multiprocessing.Value('I', 0)
    face_p = multiprocessing.Process(target=face_detection, args=(face_queue,face_quit))
    face_p.start()
    
    face_recon_queue_in = multiprocessing.Queue(1)
    face_recon_queue_out = multiprocessing.Queue()
    face_recon_quit = multiprocessing.Value('I', 0)
    face_recon_p = multiprocessing.Process(target=identify_faces, args=(face_recon_queue_in,face_recon_queue_out ,face_recon_quit))
    face_recon_p.start()
    
    try:
        while True:
            
            time.sleep(0.005)
            
            data_gatherer = {}
            
            latest_data = None
            if(face_queue.empty()):
                continue
            
            while not face_queue.empty():
                latest_data = face_queue.get(False)
                
            data_gatherer["full_frame"] = latest_data["frame"]
            
            face_frames = []
            for face in latest_data["faces"]:
                face_frames.append(latest_data["frame"][face[0]:face[2],face[1]:face[3]])
                
            if(len(face_frames) > 0):

                try:
                    
                    face_recon_queue_in.put_nowait({"frames":face_frames, "frame_id": face_data.frame_id})
                except: 
                    pass
            
            face_labels = None
            recognition_frame_id = None
            
            try :
                recognition_data = face_recon_queue_out.get_nowait()
                face_labels = recognition_data["labels"]
                recognition_frame_id = recognition_data["frame_id"]
            except:
                ...
            
            face_data.process_new_frame(latest_data["faces"], face_labels, recognition_frame_id)
            data_gatherer["faces"] = face_data

            queue.put(data_gatherer)
            
            if quit.value == 1:
                face_recon_quit.value = 1
                face_quit.value = 1
                break
            
    except Exception as e:
        print("eventloop",e)
        print(traceback.format_exc())
        
        
    face_p.join()
    face_recon_p.join()


    
    
class FakeQueue:
    def put(*args,**kwargs):
        # print("put", *args, **kwargs)
        ...
    
class FakeValue: 
    
    def __init__(self,value):
        self.value = value
        
if __name__ == "__main__":
    
    queue = FakeQueue()
    value = FakeValue(0)

    start(queue, value)
    
    print("eventloop finished")
    