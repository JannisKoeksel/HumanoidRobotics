from eventloop import start
import multiprocessing
from dataclasses import dataclass
import time
import cv2
from states.state import StateMachine, StateData
from states.handler import addHandlers
from kinematics.hubert import move, move_servo
import traceback

def run(queue):
    """
    Initialize and run the state machine with the provided data.

    This function sets up the state machine, adds necessary handlers, and then
    initiates the state machine to begin in the "idle" state.

    Args:
        queue (multiprocessing.Queue): A multiprocessing queue used to receive data for 
        the state machine.
    """
    data = StateData(queue, move, move_servo)
    
    StateMachine.stateData = data
    
    StateMachine.print()
    addHandlers()
    StateMachine("idle").run()
    
    


if __name__ == "__main__":
    """
    Main execution point for the face recognition and state machine program.

    The program uses multiprocessing to run an event loop which captures and processes 
    frames from a video feed to detect and recognize faces. Once processed, the frames 
    are displayed with bounding boxes and labels around detected faces. The program
    also interfaces with a state machine to manage certain states based on the detected 
    data. The user can terminate the program by pressing 'q'.
    """
    
    # Initialize queues and flags for inter-process communication
    event_loop_queue = multiprocessing.Queue()
    event_loop_quit = multiprocessing.Value('I', 0)
    event_loop_p = multiprocessing.Process(target=start, args=(event_loop_queue,event_loop_quit))
    event_loop_p.start()
    
    event_loop_queue.get()
    
    handler_queue = multiprocessing.Queue(maxsize=1)
    handler_quit = multiprocessing.Value('I', 0)
    handler_p = multiprocessing.Process(target=run, args=(handler_queue,))
    handler_p.start()
    
    frame_id = 0
    try:
        # Continuously process and display frames until the user terminates
        while True: 
            time.sleep(0.01)
            if(event_loop_queue.empty()): continue
            
            event_data = event_loop_queue.get()
            while not event_loop_queue.empty():
                event_data = event_loop_queue.get()
                
            frame = event_data["full_frame"]
            frame_id += 1
            
            # Annotate and display the frame with detected faces and their labels
            for face in event_data["faces"].faces.values():
                if(not face.detected ): continue
                label = face.label
                if(label == None):
                    label = "..."
                if(label == -1):
                    label = "Unknown"
                
                cv2.putText(frame, label , (face.frame[1], face.frame[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                cv2.rectangle(frame, (face.frame[1],face.frame[0]),(face.frame[3],face.frame[2]), (0,255,0), 3)
                
            cv2.imshow("Cam",frame)
            
            # Check for user input to terminate the program
            wait_key = cv2.waitKey(1)
            if wait_key & wait_key == ord('q'):
                event_loop_quit.value = 1
                print("quit")
                break
            
            # Handle the state machine data
            if not handler_queue.empty():
                try:
                    _ = handler_queue.get()
                except: 
                    pass
                
            stateData = {
                "faces": event_data["faces"].faces,
                "frame": frame,
                "frame_id": frame_id,
                "move": move,
                "initialized": True
            }
            
            handler_queue.put(stateData)
            
    except Exception as e:
        print("eventloop",e)
        print(traceback.format_exc())
        
    cv2.destroyAllWindows()
    
    handler_p.join()
    event_loop_p.join()
    
    exit(0)
