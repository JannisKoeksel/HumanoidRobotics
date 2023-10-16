from .behavior import * 


def idleHandler(state, stateData):
    print("idleHandler called")
    for i in range(10):
        data = stateData.get()
        # print("Data",data)


idle.add_handler(idleHandler)
    