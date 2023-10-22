
from typing import Callable, Dict
import serial
import  time 
import traceback
import numpy as np

MAX_MOVEMENT_THRESHOLD = 5
class StateData:
    """
    Represents the state and movement data for a robot.

    Attributes:
    - position (dict): A dictionary containing the initial positions for different parts of the robot.
    - should_follow (bool): A flag to indicate whether the robot should follow a face or not.

    Methods:
    - __init__: Initializes the object with required parameters.
    - get: Retrieves the face data from the queue and triggers the follow method if should_follow is True.
    - move: Updates the position of a given robot part by percentage.
    - move_servo: Sends command to move a specific servo to a absolute position and updates its value.
    - move_delta: Moves a specific robot part by a delta amount from its current position.
    - follow: Determines how the robot should move based on face data.
    - wait: Waits for a specified amount of seconds, while continuously processing face data.
    """

    position = {
        "B":1700,
        "P":1500,
        "T":2000,
        "S":2130,
        "E":1485,
        "G":1390
    }
    
    should_follow = True
    
    def __init__(self, queue, move, move_servo) -> None:
        """
        Initializes the StateData object.

        Parameters:
        - queue (Queue): The queue to fetch face data from.
        - move (function): Function to move a robot part to a percentage position.
        - move_servo (function): Function to move a servo to an absolute position.
        """
        self.queue = queue
        self.ser = serial.Serial('COM3', 57600)
        self.move_func = move
        self.move_servo_func = move_servo
    
    def get(self):
        """
        Fetches face data from the queue. If should_follow is True, it triggers the follow method.

        Returns:
        - dict: The face data fetched from the queue.
        """
        data = self.queue.get()
        if(self.should_follow):
            self.follow(data)
            
        return data
    
    def move(self,part,val):
        """
        Updates the position of a given robot part.

        Parameters:
        - part (str): The robot part identifier.
        - val (float): The desired position in percentage (-100 to 100).
        """
        part, pos = self.move_func(part,val, self.ser)
        self.position[part] = pos
        
        
    def move_servo(self,part,pos):
        """
        Sends command to move a specific servo to a position and updates its value.

        Parameters:
        - part (str): The identifier of the servo to move.
        - pos (float): The desired absolute position.
        """
        # print(part, pos)
        part, pos = self.move_servo_func(part,int(pos),self.ser)
        self.position[part] = pos
        
    def move_delta(self,part, pos):
        """
        Moves a specific robot part by a delta amount from its current position. Only moves a maximum amount defined by MAX_MOVEMENT_THRESHOLD

        Parameters:
        - part (str): The robot part identifier.
        - pos (float): The delta amount to change the absolute position.
        """
        current = self.position[part]
        delta = max(min(pos, MAX_MOVEMENT_THRESHOLD ), -MAX_MOVEMENT_THRESHOLD)
        self.move_servo(part, current + delta)
        
    def follow(self,data):
        """
        Determines the movements needed for the robot based on face data. 
        Makes the robot tilt and turn to keep the face centered.

        Parameters:
        - data (dict): The face data containing positions and other attributes.
        """
        center_x, center_y = (240,320)
        
        # print("___")
        
        faces = data["faces"]
        if(len(faces) ==  0): 
            self.move("B", 0)
            self.move("T", 0)
            return 
        
        
        face = list(faces.values())[0]
        if( not face.detected) : return
        x, y = face.center[-1]
        
        tilt = center_x - x 
        body =  y - center_y
        
        if(body**2 > 300):
            self.move_delta("B", body/10)
        if(tilt**2 > 300):
            self.move_delta("T", tilt/10)
            
    def wait(self,seconds):
        """
        Waits for a specified amount of seconds, while continuously processing face data.

        Parameters:
        - seconds (int): The number of seconds to wait.
        """
        start = np.datetime64("now",'s')
        seconds = int(seconds)
        while np.datetime64("now",'s') < start + np.timedelta64(seconds, "s"):
            self.get()

class StateMachine:
    """
    Represents a finite state machine to handle various states and transitions.

    Class Attributes:
    - allStates (Dict[str, State]): A dictionary that holds all possible states for the state machine.
    - stateData (StateData): The data object containing information related to the state.
    - activeState (State): The currently active state of the machine.

    Methods:
    - __init__: Initializes the state machine with the initial state.
    - activate: Activates a specified state.
    - run: Continuously runs the handler of the active state and makes transitions as required.
    - print: Prints information about all the states in the state machine.
    - add_handler: Adds a handler function to a specified state.
    """
    allStates: Dict[str,'State'] = {}
    stateData: 'StateData'
    activeState: 'State'
    def __init__(self, initial_state:str) -> None:
        """
        Initializes the StateMachine object with the initial state.

        Parameters:
        - initial_state (str): The key/name of the initial state to be activated.
        """
        self.activate(StateMachine.allStates[initial_state])
    
    def activate(self,state:'State'):
        """
        Activates a specified state, making it the active state for the machine.

        Parameters:
        - state (State): The state object to be activated.
        """
        print("current State:", state.name)
        self.activeState = state
        
    def run(self):
        """
        Runs the state machine continuously. For the active state, its handler function 
        is executed, and based on the returned transition, the next state is activated.
        """
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
            
    def print():
        """
        Prints a detailed overview of all the states present in the state machine.
        """
        for state in StateMachine.allStates.keys():
            StateMachine.allStates[state].print()

    def add_handler(state_key, handler):
        """
        Adds a handler function to a specified state.

        Parameters:
        - state_key (str): The key/name of the state to which the handler should be added.
        - handler (function): The handler function to be associated with the specified state.
        """
        StateMachine.allStates[state_key].add_handler(handler)

class Transition:
    """
    Represents a transition between two states in a finite state machine.

    Attributes:
    - incoming (State): The state from which the transition begins.
    - outgoing (State): The state to which the transition leads.
    - name (str): The name or identifier of the transition.

    Methods:
    - __init__: Initializes the Transition object with incoming and outgoing states.
    - __or__: Overrides the bitwise OR operator to set the transition name and add it to the transitions of the incoming state.
    """

    def __init__(self, incoming:'State', outgoing:'State') -> None:
        """
        Initializes the Transition object.

        Parameters:
        - incoming (State): The starting state of the transition.
        - outgoing (State): The ending state of the transition.
        """
        self.incoming = incoming
        self.outgoing = outgoing
        self.name = ""

    def __or__(self,other:str):
        """
        Overrides the bitwise OR operator. This method is used to set the name of the transition and associate it
        with the incoming state.

        Parameters:
        - other (str): The name or identifier for the transition.

        Returns:
        - Transition: Returns the transition object itself, allowing for potential chaining of operations.
        """
        self.incoming.transitions[other] = self
        self.name = other
        





class State: 
    """
    Represents a state in a finite state machine.

    Attributes:
    - name (str): The name or identifier of the state.
    - transitions (dict): A dictionary containing transitions from this state, keyed by transition name.
    - handler (Callable): A function that executes the logic associated with this state and returns the name 
                          of the next transition (or None to halt execution).

    Methods:
    - __init__: Initializes the State object with a name.
    - __rshift__: Overrides the right-shift operator to create a new transition from this state.
    - add_handler: Assigns a handler function to this state.
    - run_handler: Executes the handler and returns the associated transition.
    - print: Prints the state's name and its transitions for debugging purposes.
    """
    
    name: str; 
    # transitions: List[Transition] = []
    # incoming: List[Transition] = []
    # handler: Callable[['State'], str|None]
    
    def __init__(self, name:str) -> None:
        """
        Initializes the State object with a given name.

        Parameters:
        - name (str): The name or identifier of the state.
        """
        self.name = name
        self.transitions = {}
        StateMachine.allStates[name] = self
        
        
    def __rshift__(self,other:'State'):
        """
        Overrides the right-shift operator to create a transition from this state to another.

        Parameters:
        - other (State): The state to which the transition leads.

        Returns:
        - Transition: A new transition object.
        """
        return Transition(self,other)   
    
    def add_handler(self,handler:Callable[['State', 'StateData'], str]):
        """
        Assigns a handler function to this state.

        Parameters:
        - handler (Callable): The function to be executed when this state is active.
        """
        print(self.name, "adding handler")
        self.handler = handler
        
    def run_handler(self)-> Transition|None:
        """
        Executes the handler for this state and determines the next transition.

        Returns:
        - Transition|None: The next transition if found; otherwise, None.
        """
        try:
            res = self.handler(self, StateMachine.stateData)
        except Exception as e: 
            print(self.name , e)
            print(traceback.format_exc())
            exit(1)
        if(res):
            transition = self.transitions[res]
            if(transition.name ==  res):
                return transition
                
        print("no transition with name:", res, "in state", self.name)
    
    def print(self):
        """
        Prints the name of this state and its transitions, primarily for debugging purposes.
        """
        print(self.name)
        for key in self.transitions.keys():
            print("    ", key)
  


    


# idle = State("idle")
# scanning = State("scanning")

# idle >> scanning | "motion"

# StateMachine.print()