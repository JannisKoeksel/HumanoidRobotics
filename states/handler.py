from .behavior import * 
from ..kinematics.hubert import 


def idleHandler(state, stateData):
    print("idleHandler called")
    for i in range(10):
        data = stateData.get()
        # print("Data",data)
        for face in data["faces"].values():
            face.fid


idle.add_handler(idleHandler)
def scanHandler(state, stateData):
    


scanning.add_handler(scanHandler)