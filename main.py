import multiprocessing
from Vision import face_detection
from FaceDetection import face_detect as identify_faces
from FaceDetection.face_recon import process_frame
import cv2
import time


def start():
    face_queue = multiprocessing.Queue()
    face_quit = multiprocessing.Value('I', 0)
    face_p = multiprocessing.Process(target=face_detection, args=(face_queue,face_quit))
    face_p.start()
    
    face_recon_queue_in = multiprocessing.Queue()
    face_recon_queue_out = multiprocessing.Queue()
    face_recon_quit = multiprocessing.Value('I', 0)
    face_recon_p = multiprocessing.Process(target=identify_faces, args=(face_recon_queue_in,face_recon_queue_out ,face_recon_quit))
    face_recon_p.start()

    while True:
        time.sleep(0.01)
        if(face_queue.empty()): 
            continue
        
        latest_data = None
        
        while not face_queue.empty():
            latest_data = face_queue.get(False)
        
        
        # print(latest_data)
        frames = []
        for face in latest_data["faces"]:
            frames.append(latest_data["frame"][face[0]:face[2],face[1]:face[3]])
            
        if(len(frames) > 0):
            face_recon_queue_in.put({"frames":frames})
        
        try :
            print("labels",face_recon_queue_out.get_nowait())
        except:
            print("label exception")
        
        cv2.imshow('frame', latest_data["frame"])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            face_recon_quit.value = 1
            face_quit.value = 1
            break




if __name__ == '__main__':
    start()