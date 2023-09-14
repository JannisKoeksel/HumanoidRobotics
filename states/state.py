
from typing import Any, List,Type, Callable

class StateMashie:
    allStates: List['State'] = []
    
    activeState: 'State'
    def __init__(self, initial_state:'State') -> None:
        self.activate(initial_state)
    
    def activate(self,state:'State'):
        print("current State:", state.name)
        self.activeState = state
        
    def run(self):
        while True:
            print("running handler", self.activeState.name)
            transition = self.activeState.run_handler()
            if(transition == None):
                print("stopping StateMashie")
                return False
            print("transition is:",transition)
            print("handler returned:", transition.name)
            self.activate(transition.outgoing)
            # print("transition", transition.name, "from", transition.incoming.name, "to", transition.outgoing.name)
            
    def print() :
        
        for state in StateMashie.allStates:
            state.print()

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
        print("adding other", other)
        self.name = other
        
  
        




class State: 
    
    name: str; 
    # transitions: List[Transition] = []
    # incoming: List[Transition] = []
    # handler: Callable[['State'], str|None]
    
    def __init__(self, name:str) -> None:
        self.name = name
        self.transitions = {}
        StateMashie.allStates.append(self)
        
        
    def __rshift__(self,other:'State'):
        return Transition(self,other)   
    
    def add_handler(self,handler):
        
        self.handler = handler
        
    def run_handler(self)-> Transition|None:
        # print("running handler for", self.name)
        res = self.handler(self)
    
        if(res):
            print("res",res, "keys",self.transitions.keys())
            transition = self.transitions[res]
            print(transition.name, "found")
            if(transition.name ==  res):
                print("return", res, transition.name)
                    # print("returning transition from handler:", transition.name, "in state", self.name)
                return transition
                
        print("no transition with name:", res, "in state", self.name)
    
    def print(self):
        
        print(self.name)
        for key in self.transitions.keys():
            print("    ", key, self.transitions[key])
  




# idle = State("idle")
# scanning = State("scanning")

# idle >> scanning | "motion"

# StateMashie.print()