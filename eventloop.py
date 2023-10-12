import multiprocessing
from vision import face_detection
from FaceDetection import face_detect as identify_faces
from FaceDetection.face_recon import process_frame
import cv2
import time
from dataclasses import dataclass
from typing import Tuple, List, Dict

DISTANCE_THRESHOLD = 40
AGE_THRESHOLD = 50


old_face_locs = None

def get_center_point(face_coords):
    x = (face_coords[0]+face_coords[2])/2.
    y = (face_coords[1]+face_coords[3])/2.
    
    return x,y


def euclidean_distance(x,y,old_x,old_y):
    return ((x-old_x)**2 + (y-old_y)**2)**0.5

@dataclass
class Face: 
    
    center: List[Tuple[int,int]]
    label: str|None|int
    fid: int
    age:int 
    frame: List[int]
    detections = 0
    
    def update_center(self,x:int,y:int):
        if(len(self.center) > AGE_THRESHOLD*4):
            del self.center[0:AGE_THRESHOLD*3]
            
        self.center.append((x,y))
        
    def update_label(self,label:str|int|None):
        # self.label = label
        if(label == None): return
        
        if(self.label == None or self.label == -1):
            self.label = label
            
    def get_distance(self,x:int,y:int):
        return euclidean_distance(x,y,*self.center[-1])
    
    
class FaceData:
    frame_id = 0
    face_id = 0
    historic_data = {}
    
    def __init__(self):
        self.faces: Dict[int, 'Face'] = {}
    
    def get_id_if_exists(self, x,y):
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
        # print("process frame", face_locations)
        #update data age
        to_delete = []
        for key in self.faces.keys():
            old_face = self.faces[key]
            old_face.age += 1
            if(old_face.age > AGE_THRESHOLD):
                to_delete.append(key)
                
        #kill old 
        for key in to_delete: 
            self.faces.pop(key)
            
            
        # remove outdated historic frames
        # frames_to_delete = []
        # for key in self.historic_data.keys():
        #     if(key < self.frame_id - 100):
        #         frames_to_delete.append(key)
                
        # for key in frames_to_delete: 
        #     self.historic_data.pop(key)
        
        
        
        # print("faces:", len(face_locations), "labels:",  face_labels)
        
       
        
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
    # def face_tracker(face_locations):
    #     global old_face_locs
    #     face_locations_ids = []
        
    #     if(old_face_locs == None):
    #         old_face_locs = face_locations
    #         return []
        
    #     for face in face_locations:
    #         x,y = get_center_point(face)
    #         distances = []
            
    #         for old_face in old_face_locs:
    #             old_id, old_x, old_y = old_face
    #             distances.append((old_id, euclidean_distance(x,y,old_x,old_y)))
                
    #         min_d = 10000
    #         min_id = -1
    #         for fid,d in distances: 
    #             if(d < min_d):
    #                 min_d = d
    #                 min_id = fid
                
    #         if(min_d < DISTANCE_THRESHOLD):
    #             face_locations_ids.append(min_id)
                
    #         else: 
    #             face_locations_ids.append(face_id)
    #             face_id += 1
                
    #     old_face_locs = face_locations
        
    #     return face_locations_ids
    


def start(queue, quit):
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
    
  
    while True:
        
        # print("looping")
        time.sleep(0.005)
        
        data_gatherer = {}
        
        
        
        latest_data = None
        if(face_queue.empty()):
            continue
        
        while not face_queue.empty():
            latest_data = face_queue.get(False)
            
        data_gatherer["full_frame"] = latest_data["frame"]
        # data_gatherer["face_coordinates"] = latest_data["faces"]
        
    
        
        # print(latest_data)
        face_frames = []
        for face in latest_data["faces"]:
            face_frames.append(latest_data["frame"][face[0]:face[2],face[1]:face[3]])
            
        # print("fID:", face_data.frame_id)
        if(len(face_frames) > 0):
            # print("put:", face_data.frame_id)
            try:
                
                face_recon_queue_in.put_nowait({"frames":face_frames, "frame_id": face_data.frame_id})
            except: 
                # print("full")
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
        
        # data_gatherer["face_labels"] = face_labels
        
        # TODO voice 
        
        # print("event loop put", data_gatherer)
        # print("put")
        queue.put(data_gatherer)
        
        if quit.value == 1:
            face_recon_quit.value = 1
            face_quit.value = 1
            break



    
    
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
    