
from typing import Callable, Dict
import serial
import  time 
import traceback

MAX_MOVEMENT_THRESHOLD = 5
class StateData:

    position = {
        "B":1700,
        "P":1500,
        "T":2000,
        "S":2130,
        "E":1485,
        "G":1390
    }
    
    def __init__(self, queue, move, move_servo) -> None:
        self.queue = queue
        self.ser = serial.Serial('COM3', 57600)
        self.move_func = move
        self.move_servo_func = move_servo
    
    def get(self):
        return self.queue.get()
    
    def move(self,part,val):
        part, pos = self.move_func(part,val, self.ser)
        self.position[part] = pos
        
        
    def move_servo(self,part,pos):
        print(part, pos)
        part, pos = self.move_servo_func(part,int(pos),self.ser)
        self.position[part] = pos
        
    def move_delta(self,part, pos):
        current = self.position[part]
        delta = max(min(pos, MAX_MOVEMENT_THRESHOLD ), -MAX_MOVEMENT_THRESHOLD)
        self.move_servo(part, current + delta)

class StateMachine:
    allStates: Dict[str,'State'] = {}
    stateData: 'StateData'
    activeState: 'State'
    def __init__(self, initial_state:str) -> None:
        self.activate(StateMachine.allStates[initial_state])
    
    def activate(self,state:'State'):
        print("current State:", state.name)
        self.activeState = state
        
    def run(self):
        while True:
            # print("running handler", self.activeState.name)
            transition = self.activeState.run_handler()
            if(transition == None):
                print("stopping StateMachine")
                return False
            # print("transition is:",transition)
            # print("handler returned:", transition.name)
            self.activate(transition.outgoing)
            # print("transition", transition.name, "from", transition.incoming.name, "to", transition.outgoing.name)
            
    def print() :
        
        for state in StateMachine.allStates.keys():
            StateMachine.allStates[state].print()
            
    def add_handler(state_key, handler):
        StateMachine.allStates[state_key].add_handler(handler)

class Transition:
    
    # name: str; 
    # incoming: 'State'
    # outgoing: 'State'
    
    
    def __init__(self, incoming:'State', outgoing:'State') -> None:
        self.incoming = incoming
        self.outgoing = outgoing
        self.name = ""
        
    
    def __or__(self,other:str):
        self.incoming.transitions[other] = self
        # print("adding other", other)
        self.name = other
        
  
        




class State: 
    
    name: str; 
    # transitions: List[Transition] = []
    # incoming: List[Transition] = []
    # handler: Callable[['State'], str|None]
    
    def __init__(self, name:str) -> None:
        self.name = name
        self.transitions = {}
        StateMachine.allStates[name] = self
        
        
    def __rshift__(self,other:'State'):
        return Transition(self,other)   
    
    def add_handler(self,handler:Callable[['State', 'StateData'], str]):
        print(self.name, "adding handler")
        self.handler = handler
        
    def run_handler(self)-> Transition|None:
        # print("running handler for", self.name)
        
        try:
            res = self.handler(self, StateMachine.stateData)
        except Exception as e: 
            print(self.name , e)
            print(traceback.format_exc())
            exit(1)
        if(res):
            # print("res",res, "keys",self.transitions.keys())
            transition = self.transitions[res]
            # print(transition.name, "found")
            if(transition.name ==  res):
                # print("return", res, transition.name)
                    # print("returning transition from handler:", transition.name, "in state", self.name)
                return transition
                
        print("no transition with name:", res, "in state", self.name)
    
    def print(self):
        
        print(self.name)
        for key in self.transitions.keys():
            print("    ", key)
  


    


# idle = State("idle")
# scanning = State("scanning")

# idle >> scanning | "motion"

# StateMachine.print()