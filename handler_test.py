from eventloop import start
import multiprocessing
from dataclasses import dataclass
import time
import cv2
from states.state import StateMachine, StateData
from states.handler import addHandlers
from kinematics.hubert import move, move_servo

def run(queue):
    
    data = StateData(queue, move, move_servo)
    StateMachine.stateData = data
    StateMachine.print()
    addHandlers()
    
    
    StateMachine("idle").run()
    
class FakeQueue:
    def put(*args,**kwargs):
        # print("put", *args, **kwargs)
        ...
    def get(): 
        stateData = {
            "faces": {},
            "frame": [],
            "frame_id": 5,
            "initialized": True
        }
        return stateData
        
class FakeValue: 
    
    def __init__(self,value):
        self.value = value
        
if __name__ == "__main__":
    
    queue = FakeQueue()
  

    run(queue)
    

    
    print("eventloop finished")