from ..kinematics.hubert import move_servo
def faceTracking(data):
    for face in data["faces"].values():
        #Follow the first unknown face detected change to accomodate the scenario when there are some recognized but no unknown faces.
        if face.label != None:
            faceCoords = face.center
    positionData = data["position"].values()
    headPos = positionData.headPos
    bodyPos = positionData.bodyPos
    scaleFactor = 1
    centerImage = [320,240]
    diffX = faceCoords[0]-centerImage[0]
    diffY = faceCoords[1] - centerImage[1]
    newBodyPos = scaleFactor*diffX+bodyPos
    newHeadPos = scaleFactor*diffY+headPos
    move_servo('B',newBodyPos)
    move_servo('T', newHeadPos)
    return [newBodyPos,newHeadPos]