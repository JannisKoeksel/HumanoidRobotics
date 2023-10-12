from eventloop import start
import multiprocessing
from dataclasses import dataclass
import time
import cv2



if __name__ == "__main__":
    
    event_loop_queue = multiprocessing.Queue()
    event_loop_quit = multiprocessing.Value('I', 0)
    event_loop_p = multiprocessing.Process(target=start, args=(event_loop_queue,event_loop_quit))
    event_loop_p.start()
    
    
    
    
    
    while True: 
        time.sleep(0.01)
        if(event_loop_queue.empty()): continue
        
        event_data = event_loop_queue.get()
        while not event_loop_queue.empty():
            event_data = event_loop_queue.get()
            
        
        
        frame = event_data["full_frame"]
        
        # for face in event_data["faces"].faces.values():
        #     print(face.label)
            
        for face in event_data["faces"].faces.values():
            if(face.age > 2): continue
            if(face.detections  < 5): continue
            label = face.label
            if(label == None):
                label = "..."
            if(label == -1):
                label = "Unknown"
            
            cv2.putText(frame, label , (face.frame[1], face.frame[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            cv2.rectangle(frame, (face.frame[1],face.frame[0]),(face.frame[3],face.frame[2]), (0,255,0), 3)
            
        # print("frame")
        cv2.imshow("Cam",frame)
        
        wait_key = cv2.waitKey(1)
        if wait_key & wait_key == ord('q'):
            event_loop_quit.value = 1
            print("quit")
            break
        
    cv2.destroyAllWindows()
    
    exit(0)